from nltk.parse.pchart import LongestChartParser
from nltk.parse.generate import generate
from nltk.grammar import PCFG
import numpy as np
import regex

def generate_language(
    grammar: PCFG,
    max_depth: int | None = None
) -> list[tuple[list[str], np.float64]]:
    """
    Generate all sequences and subsequences from an NLTK PCFG.

    Subsequence probabilities are found by summing over all whole
    sequences beginning with the specific subsequence.

    Args
    ----
    grammar : nltk.grammar.PCFG
        The probabilistic context-free grammar to generate sequences from.
    max_depth : int | None (default `None`)
        `depth` argument to `nltk.parse.generate.generate`.

    Returns
    -------
    list
        A list of tuples, each consisting of the sequence as
        a list of strings and its associated probability in the
        PCFG.
    """
    parser = LongestChartParser(grammar)

    # generate all possible sequences from the grammar
    language: list[tuple[list[str], np.float64]] = []
    for sequence in generate(grammar, depth = max_depth):
        sequence_prob = next(parser.parse(sequence)).prob()
        language.append((sequence, np.float64(sequence_prob)))

    # add subsequences to the language
    sub_sequences = []
    sub_sequence_probs = []
    for (language_sequence, _) in language:
        for i in range(1, len(language_sequence)):
            sub_sequence = language_sequence[:i]
            if sub_sequence in sub_sequences:
                continue

            sub_sequence_prob = np.float64(0.0)
            for (sequence, prob) in language:
                if sequence[:i] == sub_sequence:
                    sub_sequence_prob += prob

            sub_sequences.append(sub_sequence)
            sub_sequence_probs.append(sub_sequence_prob)

    language += list(zip(sub_sequences, sub_sequence_probs))
    return language

def save_language(
    language: list[tuple[list[str], np.float64]],
    filename: str
):
    content = "\n".join([
        f"{' '.join(sequence)}:{prob}"
        for (sequence, prob) in language
    ])

    with open(filename, "w") as f:
        f.write(content)


def read_language(filename: str) -> list[tuple[list[str], np.float64]]:
    with open(filename, "r") as f:
        lines = f.readlines()

    language: list[tuple[list[str], np.float64]] = []
    for line in lines:
        line = line.strip()
        groups = regex.match(r'(.+):([0-9\.\-e]+)', line)
        sequence = groups[1].split(" ")
        prob = np.float64(groups[2])
        language.append((sequence, prob))

    return language


if __name__ == "__main__":
    from grammars import gen_russian_grammar_exp2
    pcfg_russian = PCFG.fromstring(
        gen_russian_grammar_exp2(
            p_src = 0.58, 
            p_src_local = 0.99,
            p_src_case_marked = 0.9,
            p_orc_local = 0.36,
            p_orc_case_marked = 0.83,
            p_one_arg = 0.97, 
            p_adj_interveners = 0.16, 
            p_one_adj = 0.95
        )
    )

    language = generate_language(pcfg_russian)
    print(language)
    print("------------------------------")
    save_language(language, "language_russian.txt")
    language_read_in = read_language("language_russian.txt")
    print(language_read_in)