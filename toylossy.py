from nltk.grammar import PCFG
from nltk.parse.pchart import LongestChartParser
from nltk.parse.generate import generate
import numpy as np
from abc import ABC, abstractmethod

def print_if_true(text, flag):
    if flag:
        print(text)

class LossyContextModel(ABC):
    """
    An abstract class for a simple lossy-context surprisal model.

    The underlying language model is given as a probabilistic context-free grammar
    as implemented in `nltk`. The language is first generated by creating all sequences
    from the grammar, then adding all subsequences (a rule S -> NP PP V thus gets three items in
    the language: NP, NP PP and NP PP V).

    To implement the class the method `get_distortion_probability` has to be specified, which returns
    the probability of a sequence `true_sequence` being distorted as a certain other sequence `distortion`.
    A distortion is the true context with zero or more words removed.

    The argument `max_depth` is passed to `nltk.parse.generate`.
    """
    def __init__(self, grammar: PCFG, max_depth: int = None):
        parser = LongestChartParser(grammar)

        # generate all possible sequences from the grammar
        self.language: list[tuple[list[str], np.float64]] = []
        for sequence in generate(grammar, depth = max_depth):
            sequence_prob = next(parser.parse(sequence)).prob()
            self.language.append((sequence, np.float64(sequence_prob)))

        # add subsequences to the language
        sub_sequences = []
        sub_sequence_probs = []
        for (language_sequence, _) in self.language:
            for i in range(1, len(language_sequence)):
                sub_sequence = language_sequence[:i]
                if sub_sequence in sub_sequences:
                    continue

                sub_sequence_prob = np.float64(0.0)
                for (sequence, prob) in self.language:
                    if sequence[:i] == sub_sequence:
                        sub_sequence_prob += prob

                sub_sequences.append(sub_sequence)
                sub_sequence_probs.append(sub_sequence_prob)

        self.language += list(zip(sub_sequences, sub_sequence_probs))


    def get_prob(self, sequence: list[str]) -> np.float64:
        """Calculate the a priori probability of `sequence` [p_L(sequence)]."""
        for (language_sequence, probability) in self.language:
            if language_sequence == sequence:
                return probability
            
        return np.float64(0.0)
    
    def get_conditional_prob(self, sequence: list[str]) -> np.float64:
        """Calculate the conditional probability of `sequence[-1]` given `sequence[:-1]`."""
        return self.get_prob(sequence)/self.get_prob(sequence[:-1]) if self.get_prob(sequence[:-1]) != 0 else np.float64(0.0)


    def get_distortions(self, sequence: list[str]) -> list[tuple[list[str], np.float64]]:
        """
        Generate all possible memory representations/distortions from a given sequence.

        Args
        ----
        sequence : list[str]
            A sequence of words from the grammar.

        Returns
        -------
        list[tuple[list[str], np.float64]]
            A list of tuples with the form (distortion, distortion_probability)
        """
        distortions = []
        # length is the length of the distorted sequence
        for length in range(len(sequence), -1, -1):
            distortions += [(distortion, self.get_distortion_probability(sequence, distortion))
                            for distortion in self._get_distortions_of_length(sequence, length)]
            
        return distortions


    @abstractmethod
    def get_distortion_probability(self, true_sequence: list[str], distortion: list[str]) -> np.float64: ...


    def _get_distortions_of_length(self, sequence: list[str], length: int) -> list[list[str]]:
        if length == len(sequence):
            return [sequence]
        elif length == 0:
            return [[]]

        distortions = []
        for (i, word) in enumerate(sequence):
            if length == 1:
                distortions.append([word])
            else:
                distortions += [[word] + distortion for distortion in self._get_distortions_of_length(sequence[i+1:], length - 1)]

        return distortions


    def get_reconstructions(self, distortion: list[str]) -> list[list[str]]:
        """
        Find all language sequences which could have given rise to the given memory
        representation/distortion.

        Args
        ----
        distortion : list[str]
            A sequence of words from the grammar representing a
            distorted context.

        Returns
        -------
        list[list[str]]
            All language sequences which contain all of the words in
            `distortion`. 
        """
        reconstructions = []
        for (reconstruction, _) in self.language:
            if all([word in reconstruction for word in distortion]):
                reconstructions.append(reconstruction)

        return reconstructions


    def calculate_processing_difficulty(self, sequence: list[str], verbose = False) -> np.float64:
        """
        Calculate the predicted processing difficulty of the last word in `sequence`.

        See the thesis for an explanation of lossy-context surprisal and details about this implementation.

        The edge case of a one-length sequence (that is, there is no context) is handled by returning the
        surprisal of that symbol starting a sequence according to the language model.

        Args
        ----
        sequence : list[str]
            A sequence of words from the grammar, with the last being the word for which
            processing difficulty is calculated.

        verbose : bool
            Set to `True` for detailed output.

        Returns
        -------
        np.float64
            The processing difficulty.
        """

        if len(sequence) == 1:
            return -np.log2(self.get_prob(sequence))

        print_if_true(f"True context: {' '.join(sequence[:-1])}", flag = verbose)
        target_word = sequence[-1]
        processing_difficulty = np.float64(0.0)
        for (distortion, probability) in self.get_distortions(sequence[:-1]):
            print_if_true(f"Current distortion: {distortion}", flag = verbose)
            print_if_true(f"p(r|c) = {probability}", flag = verbose)
            if probability == 0:
                continue

            average_prob = np.float64(0.0)
            normaliser = np.float64(0.0)
            for reconstruction in self.get_reconstructions(distortion):
                reconstruction_with_target = reconstruction + [target_word]
                context_probability = self.get_prob(reconstruction)
                target_probability = self.get_prob(reconstruction_with_target)/context_probability

                print_if_true(f" ## Possible reconstructed context: {' '.join(reconstruction)}", flag = verbose)

                print_if_true(f" ## Reconstructing sentence as: {' '.join(reconstruction_with_target)}", flag = verbose)
                distortion_probability = self.get_distortion_probability(reconstruction, distortion)
                print_if_true(f" ## p(r|~c) = {distortion_probability}", flag = verbose)

                print_if_true(f" ## p_L(~c) = {context_probability}", flag = verbose)
                print_if_true(f" ## p_L(w|~c) = {target_probability}\n", flag = verbose)

                average_prob += context_probability * distortion_probability * target_probability
                normaliser += context_probability * distortion_probability

            average_prob /= normaliser

            print_if_true(f"E[p(w|~c)] = {average_prob}", verbose)

            processing_difficulty += -np.log2(average_prob) * probability
            print_if_true("", flag = verbose)

        print_if_true(f"D(w|c) = {processing_difficulty}", verbose)
        return processing_difficulty
    

    def calculate_sequence_processing_difficulty(self, sequence: list[str]) -> np.array:
        return np.array([self.calculate_processing_difficulty(sequence[:i+1]) for i in range(len(sequence))])


class SimpleDeletionModel(LossyContextModel):
    """
    A simple implementation with a memory model which removes
    words randomly with probability `deletion_rate`.
    """
    def __init__(self, grammar: PCFG, deletion_rate: float, max_depth: int = None):
        super().__init__(grammar, max_depth = max_depth)

        self.deletion_rate = np.float64(deletion_rate)

    def get_distortion_probability(self, true_sequence: list[str], distortion: list[str]) -> np.float64:
        return self.deletion_rate**(len(true_sequence) - len(distortion)) * (1-self.deletion_rate)**len(distortion)


class SurprisalModel(LossyContextModel):
    """
    A surprisal model implemented as a special case of
    lossy-context surprisal with no loss of information.
    """
    def __init__(self, grammar: PCFG, max_depth: int = None):
        super().__init__(grammar, max_depth = max_depth)

    def get_distortion_probability(self, true_sequence: list[str], distortion: list[str]) -> np.float64:
        return np.float64(1.0 if distortion == true_sequence else 0.0)
    

class ProgressiveNoiseModel(LossyContextModel):
    """
    An implementation with a progressive noise model.

    The probability of word j being retained with word i as the last word in the context is given as

    `max_retention_probability*rate_falloff**(i-j)`
    """
    def __init__(self, grammar: PCFG, max_retention_probability: float, rate_falloff: float, max_depth: int = None):
        super().__init__(grammar, max_depth = max_depth)

        self.max_retention_probability = np.float64(max_retention_probability)
        self.rate_falloff = np.float64(rate_falloff)

    def get_distortion_probability(self, true_sequence: list[str], distortion: list[str]) -> np.float64:
        prob = np.float64(1.0)
        for (i, word) in enumerate(true_sequence):
            steps_back = len(true_sequence) - (i+1)
            retention_probability = self.max_retention_probability*self.rate_falloff**steps_back
            if word in distortion:
                prob *= retention_probability
            else:
                prob *= 1-retention_probability

        return prob
    
    
    def set_max_retention_probability(self, max_retention_probability: np.float64):
        self.max_retention_probability = max_retention_probability


    def set_rate_falloff(self, rate_falloff: np.float64):
        self.rate_falloff = rate_falloff