# treemaker

A Python library for creating a Newick formatted tree from a set of classification strings (e.g. a taxonomy)

[![Build Status](https://travis-ci.org/SimonGreenhill/treemaker.svg?branch=master)](https://travis-ci.org/SimonGreenhill/treemaker)
[![Coverage Status](https://coveralls.io/repos/SimonGreenhill/treemaker/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonGreenhill/treemaker?branch=master)
[![DOI](https://zenodo.org/badge/22704/SimonGreenhill/treemaker.svg)](https://zenodo.org/badge/latestdoi/22704/SimonGreenhill/treemaker)
[![status](http://joss.theoj.org/papers/19eae6958062fc8a72d8a02efdaf8b23/status.svg)](http://joss.theoj.org/papers/19eae6958062fc8a72d8a02efdaf8b23)

```treemaker``` is a Python library to convert a text-based classification schema into a Newick file for use in phylogenetic and bioinformatic programs.

Research in linguistics or cultural evolution often produces or uses tree taxonomies or classifications. However, these are usually not in a format readily available for use in programs that can understand and manipulate trees. For example, the global taxonomy of languages published by the [Ethnologue](https://www.ethnologue.com/) classifies languages into families and subgroups using a taxonomy string e.g. the language [Kalam](https://www.ethnologue.com/language/kmh) is classified as "Trans-New Guinea, Madang, Kalam-Kobon", while [Mauwake](https://www.ethnologue.com/language/mhl) is classified as "Trans-New Guinea, Madang, Croisilles, Pihom", and [Kare](https://www.ethnologue.com/language/kmf) is "Trans-New Guinea, Madang, Croisilles, Kare". This classification indicates that while all these languages are part of the Madang subgroup of the Trans-New Guinea language family, Kare and Mauwake are more closely related (as they belong to the Croisilles subgroup).

Other publications use a tabular indented format to demarcate relationships, such as the example in Figure 1 from Stephen Wurm's classification of his proposed Yele-Solomons language phylum (Wurm 1975).

Both the taxonomy string and tabular format however are hard to load into software packages that can analyse, compare, visualise and manipulate trees. ```treemaker``` aims to make this easy by converting taxonomic data into [Newick](https://en.wikipedia.org/wiki/Newick_format) and Nexus (Maddison 1997) formats commonly used by phylogenetic manipulation programs.

## Converting a Taxonomy to a Tree:

```treemaker``` can convert a text file with a taxonomy to a tree. These taxonomies can easily be obtained from Ethnologue or manually entered, such as this example from Wurm's (outdated) classification of Yele-Solomons in Figure 1:

```text
Bilua       Yele-Solomons, Central Solomon
Baniata     Yele-Solomons, Central Solomon
Lavukaleve  Yele-Solomons, Central Solomon
Savosavo    Yele-Solomons, Central Solomon
Kazukuru    Yele-Solomons, Kazukuru
Guliguli    Yele-Solomons, Kazukuru
Dororo      Yele-Solomons, Kazukuru
Yele        Yele-Solomons
```

``treemaker`` can then generate a Newick representation:

```text
((Baniata,Bilua,Lavukaleve,Savosavo),(Dororo,Guliguli,Kazukuru),Yele);
```

...which can then be loaded into phylogenetic programs to visualise or manipulate as in Figure 2.

```treemaker``` has been used to enable the analyses in (Bromham et al. 2018), and a number of forthcoming articles.


![Example of a language taxonomy in indented format from Wurm (1975).](wurm1975.png)

![Tree visualisation of the relationships between the putative Yele-Solomons languages.](tree.png)


## Installation:

Installation is only a pip install away:

```shell
pip install treemaker
```

Or from git:

```shell
git clone https://github.com/SimonGreenhill/treemaker/ treemaker
cd treemaker
python setup.py install
```

## Usage: Command line:

Basic usage: 

```shell
> treemaker

usage: treemaker [-h] [-o OUTPUT] [-m {nexus,newick}] [--labels] input
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
(LangD,(LangA,LangB),LangC);

# with nodelabels:
> treemaker --labels classification.txt
(LangD,(LangA,LangB)Germanic,LangC)Indo-European;

> treemaker -m nexus classification.txt

#NEXUS

begin trees;
   tree root = (LangD,(LangA,LangB),LangC);
end;
```

To write to file:

```shell
> treemaker classification.txt
(LangD,(LangA,LangB),LangC);

> treemaker classification.txt -o classification.nex
```


## Usage: Library:

```python
from treemaker import TreeMaker
```

### generate a tree manually:

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

### Add from a list:

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

## API Documentation:

The API is [documented here](https://simongreenhill.github.io/treemaker/build/html/index.html).

## Running treemaker's tests:

To run treemaker's tests simply run:

```shell
> make test
# or
> python setup.py test
# or
> python treemaker/test_treemaker.py
```


## Version History:

* v1.4: fix bug with no terminating semicolon in nexus file output.
* v1.3: add nodelabels support, add some rudimentary input checking.

## Support:

For questions on how to use or update this, feel free to [open an issue](https://github.com/SimonGreenhill/treemaker/issues). I'll get to it as soon as I can. 

## Acknowledgements:

Thank you to [Richard Littauer](https://github.com/RichardLitt), [Mitsuhiro Nakamura](https://github.com/mnacamura), and [Dillon Niederhut](https://github.com/deniederhut).

## References:

* Bromham, Lindell, Xia Hua, Marcel Cardillo, Hilde Schneemann, & Simon J. Greenhill. 2018. “[Parasites and Politics: Why Cross-Cultural Studies Must Control for Relatedness, Proximity and Covariation](https://doi.org/10.1098/rsos.181100).” Open Science 5 (8). https://doi.org/10.1098/rsos.181100.
* Maddison, D R, D L Swofford, & Wayne P. Maddison. 1997. “[Nexus: An Extensible File Format for Systematic Information](https://doi.org/10.1093/sysbio/46.4.590).” Systematic Biology 46 (4): 590–621. https://doi.org/10.1093/sysbio/46.4.590.
* Wurm, S. A. 1975. “[The East Papuan Phylum in General](https://doi.org/http://dx.doi.org/10.15144/PL-C38).” In New Guinea Area Languages and Language Study: Papuan Languages and the New Guinea Linguistic Scene, edited by S. A. Wurm. Canberra: Pacific Linguistics. https://doi.org/http://dx.doi.org/10.15144/PL-C38.
