# toylossy
This is the repository for the implementation of lossy-context surprisal accompanying my bachelor thesis.

## Installation
The following Python libraries are required for the model itself:
```
nltk
numpy
```

The following packages are additionally used in the notebook `toylossy_demo.ipynb`:
```
pandas
seaborn
matplotlib
tqdm
```

## Usage
The class `LossyContextModel` is implemented as an abstract class for which only the method `get_distortion_probability` has to be defined. It takes a true sequence and some distortion and returns the probability of the true sequence having been distorted in that way according to the chosen noise model.

There are three models already implemented: the progressive noise model used in the thesis (`ProgressiveNoiseModel`), a model with a constant deletion rate (`SimpleDeletionModel`) and a basic surprisal model (`SurprisalModel`).

A model is initialised with a PCFG as the language model (a `nltk.grammar.PCFG`). To calculate processing difficulty, `LossyContextModel` offers the method `calculate_processing_difficulty`, which takes a sequence as a list of symbols from the grammar and returns the predicted processing difficulty in bits. At this point, this method does **not** check if every symbol is actually part of the grammar, so carefully check if all symbols in the sequence are contained in the grammar if the results seem odd.

All commands used to generate the plots in the thesis can be found in `toylossy_demo.ipynb`.

The probabilities used to initiate the PCFGs for the different experiments were, mostly, calculated from Universal Dependencies corpora. The queries, frequencies and how the probabilities were calculated can be found in the file `pcfg_probs.md`
