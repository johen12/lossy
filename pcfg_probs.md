# PCFGs
The language models were defined in the form of probabilistic context-free grammars. In order to find the probabilities necessary, the [PML Tree Query Engine](https://lindat.mff.cuni.cz/services/pmltq/#!/treebanks) was used, which offers its own query language.

## Russian
The following probabilities had to be calculated from corpus data (the rest had been found by Levy et al., 2013):

 - $p(\text{One argument})=\frac{\text{at least one argument}-\text{at least two arguments}}{\text{at least one argument}}$
 - $p(\text{Adjunct intervener})=\frac{\text{at least one intv}}{\text{any number of intvs}}$
 - $p(\text{One adjunct intervener})=\frac{\text{at least one intv}-\text{at least two intvs}}{\text{at least one intv}}$

|                                   | Frequency |
| --------------------------------- | --------- |
| $\text{at least one argument}$    | 1109      |
| $\text{at least two arguments}$   | 36        |
| $\text{any number of intvs}$      | 5851      |
| $\text{at least one intv}$        | 925       |
| $\text{at least two intvs}$       | 49        |


 ### Queries
 *Any number of interveners:*
```
a-node $v := [
  tag="VERB",
  deprel = "acl:relcl",
  child a-node $r := [
    tag = "PRON",
    lemma = "который"
  ],
] >> count()
```

| SynTagRus | GSD | PUD | Taiga | *Total* |
| --------- | --- | --- | ----- | ------- |
| 5110      | 347 | 122 | 272   | 5851    |


*At least one adjunct intervener:*
```
a-node $v := [
  tag="VERB",
  deprel = "acl:relcl",
  child a-node $r := [
    tag = "PRON",
    lemma = "который",
  ],
  
  child a-node [
    tag = "ADV",
    deprel = "advmod",
    order-follows $r,
    order-precedes $v
  ]
] >> count()
```

| SynTagRus | GSD | PUD | Taiga | *Total* |
| --------- | --- | --- | ----- | ------- |
| 845       | 32  | 8   | 40    | 925     |


*At least two adjunct interveners:*
```
a-node $v := [
  tag="VERB",
  deprel = "acl:relcl",
  child a-node $r := [
    tag = "PRON",
    lemma = "который",
  ],
  
  child a-node [
    tag = "ADV",
    deprel = "advmod",
    order-follows $r,
    order-precedes $v
  ],
  
  child a-node [
    tag = "ADV",
    deprel = "advmod",
    order-follows $r,
    order-precedes $v
  ],
] >> count()
```

| SynTagRus | GSD | PUD | Taiga | *Total* |
| --------- | --- | --- | ----- | ------- |
| 45        | 3   | 0   | 1     | 49      |

*At least one argument:*
```
a-node $v := [
  tag="VERB",
  deprel = "acl:relcl",
  child a-node $r := [
    tag = "PRON",
    lemma = "который",
  ],
  
  child a-node [
	tag = "NOUN",
    deprel = "obj",
  ],
] >> count()
```

| SynTagRus | GSD | PUD | Taiga | *Total* |
| --------- | --- | --- | ----- | ------- |
| 947       | 85  | 27  | 50    | 1109    |

*At least two arguments:*
```
a-node $v := [
  tag="VERB",
  deprel = "acl:relcl",
  child a-node $r := [
    tag = "PRON",
    lemma = "который",
  ],
  
  child a-node [
	tag = "NOUN",
    deprel = "obj",
  ],

  child a-node [
    tag = "NOUN",
    deprel = "iobj"
  ]
] >> count()
```

| SynTagRus | GSD | PUD | Taiga | *Total* |
| --------- | --- | --- | ----- | ------- |
| 32        | 1   | 2   | 1     | 36      |

## Hindi/Persian
The following probabilities had to be specified for the Hindi/Persian grammar.

 - $p(\text{CP}) = \frac{\text{CP}}{\text{CP}+\text{SP}}$
 - $p(\text{SP Interveners}) = \frac{\text{SP at least one intv}}{\text{SP}}$
 - $p(\text{SP Short}) = \frac{\text{SP at least one intv} - \text{SP at least two intv}}{\text{SP  at least one intv}}$
 - $p(\text{CP Interveners}) = \frac{\text{CP at least one intv}}{\text{CP}}$
 - $p(\text{CP Short}) = \frac{\text{CP at least one intv} - \text{CP at least two intv}}{\text{CP  at least one intv}}$

### Hindi results
|                      | HDTB | PUD | Total |
| -------------------- | ---- | --- | ----- |
| SP                   | 2291 | 493 | 2784  |
| CP                   | 2808 | 2   | 2810  |
| SP at least one intv | 122  | 40  | 162   |
| SP at least two intv | 1    | 0   | 1     |
| CP at least one intv | 138  | 2   | 140   |
| CP at least two intv | 0    | 0   | 0     |

### Persian results
|                      | PerDT | Seraji | Total |
| -------------------- | ----- | ------ | ----- |
| SP                   | 3748  | 505    | 4253  |
| CP                   | 9597  | 1108   | 10705 |
| SP at least one intv | 80    | 17     | 97    |
| SP at least two intv | 1     | 0      | 1     |
| CP at least one intv | 2     | 0      | 2     |
| CP at least two intv | 0     | 0      | 0     |

### Queries
The following queries work for Persian. Because of labeling differences between Hindi and Persian, `compound:lvc` has to be changed to just `compound` for the queries to work for the Hindi corpora.

#### Simple predicates
```
a-node $v := [
	tag = "VERB",
	deprel = "root",
	child a-node [
		deprel = "obj",
		tag = "NOUN"
	],
	!child a-node [
	  deprel = "compound:lvc",
	]
] >> count()
```

*With at least one intervener:*
```
a-node $v := [
	tag = "VERB",
	deprel = "root",
	child a-node $o := [
		deprel = "obj",
		tag = "NOUN"
	],
	!child a-node [
	  deprel = "compound:lvc",
	],
	child a-node [
		order-precedes $v,
		order-follows $o,
		deprel = "advmod"
	]
] >> count()
```

*With two interveners:*
```
a-node $v := [
	tag = "VERB",
	deprel = "root",
	child a-node $o := [
		deprel = "obj",
		tag = "NOUN"
	],
	!child a-node [
	  deprel = "compound:lvc",
	],
	child a-node [
		order-precedes $v,
		order-follows $o,
		deprel = "advmod"
	],
	child a-node [
		order-precedes $v,
		order-follows $o,
		deprel = "advmod"
	]
] >> count()
```

#### Complex predicates
```
a-node $v := [
	tag = "VERB",
	deprel = "root",
	!child a-node [
		deprel = "obj",
	],
	child a-node [
	  deprel = "compound:lvc",
	  tag = "NOUN"
	]
] >> count()
```

*With one intervener:*
```
a-node $v := [
	tag = "VERB",
	deprel = "root",
	!child a-node [
		deprel = "obj",
	],
	child a-node $o := [
	  deprel = "compound:lvc",
	  tag = "NOUN"
	],
	child a-node [
		order-precedes $v,
		order-follows $o,
		deprel = "advmod"
	]
] >> count()
```

*With two interveners:*
```
a-node $v := [
	tag = "VERB",
	deprel = "root",
	!child a-node [
		deprel = "obj",
	],
	child a-node $o := [
	  deprel = "compound:lvc",
	  tag = "NOUN"
	],
	child a-node [
		order-precedes $v,
		order-follows $o,
		deprel = "advmod"
	],
	child a-node [
		order-precedes $v,
		order-follows $o,
		deprel = "advmod"
	]
] >> count()
```