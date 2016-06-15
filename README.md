# treemaker

A python library for creating a Newick formatted tree from a set of classification strings (e.g. a taxonomy)

[![Build Status](https://travis-ci.org/SimonGreenhill/treemaker.svg?branch=master)](https://travis-ci.org/SimonGreenhill/treemaker)
[![Coverage Status](https://coveralls.io/repos/SimonGreenhill/treemaker/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonGreenhill/treemaker?branch=master)
[![DOI](https://zenodo.org/badge/22704/SimonGreenhill/treemaker.svg)](https://zenodo.org/badge/latestdoi/22704/SimonGreenhill/treemaker)


## Usage: Command line

Basic usage: 

```shell
> treemaker

usage: treemaker [-h] filename
```

e.g. Given a text file:

```
LangA   Indo-European, Germanic
LangB   Indo-European, Germanic
LangC   Indo-European, Romance
LangD   Indo-European, Anatolian
```

... then you can build a taxonomy/classification tree from that as follows:

```shell
> treemaker classification.txt
(LangD,(LangA,LangB),LangC)

> treemaker -m nexus classification.txt

#NEXUS

begin trees;
   tree root = (LangD,(LangA,LangB),LangC);
end;
```

To write to file:

```shell
> treemaker classification.txt
(LangD,(LangA,LangB),LangC)

> treemaker classification.txt -o classification.nex
```


## Usage: Library

```python
from treemaker import TreeMaker
```

### generate a tree manually

```python
from treemaker import TreeMaker

t = TreeMaker()
t.add('A1', 'family a, subgroup 1')
t.add('A2', 'family a, subgroup 2')
t.add('B1a', 'family b, subgroup 1')
t.add('B1b', 'family b, subgroup 1')
t.add('B2', 'family b, subgroup 2')

print(t.write())
```

### Add from a list

```python
from treemaker import TreeMaker

taxa = [
    ('A1', 'family a, subgroup 1'),
    ('A2', 'family a, subgroup 2'),
    ('B1a', 'family b, subgroup 1'),
    ('B1b', 'family b, subgroup 1'),
    ('B2', 'family b, subgroup 2'),
]

t = TreeMaker()
t.add_from(taxa)

print(t.write())

```



