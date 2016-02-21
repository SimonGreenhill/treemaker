# treemaker

A python library for creating a Newick formatted tree from a set of classification strings (e.g. a taxonomy)

[![Build Status](https://travis-ci.org/SimonGreenhill/treemaker.svg?branch=master)](https://travis-ci.org/SimonGreenhill/treemaker)
[![Coverage Status](https://coveralls.io/repos/SimonGreenhill/treemaker/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonGreenhill/treemaker?branch=master)


## Usage: Command line


Basic usage: 

```shell
> treemaker

usage: treemaker [-h] filename
```

Construct tree for filename
```shell
> treemaker 

taxon1              0.2453
taxon2              0.2404
taxon3              0.2954
...
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



