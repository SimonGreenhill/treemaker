---
title: 'TreeMaker:  A Python tool for constructing a newick formatted tree from a set of classifications.'
tags:
  - phylogenetics
  - newick
  - tree
authors:
 - name: Simon J Greenhill
   orcid: 0000-0001-7832-6156
   affiliation: "1, 2"
affiliations:
 - name: Department of Linguistic and Cultural Evolution, Max Planck Institute for the Science of Human History, Jena, Germany.
   index: 1
 - name: ARC Centre of Excellence for the Dynamics of Language, Australian National University, Canberra, Australia.
   index: 2
date: 27 September 2018
bibliography: paper.bib
---

# Summary

```TreeMaker``` is a python program to convert a text-based classification schema into a Newick file for use in phylogenetic and bioinformatic programs.

Often research in linguistics or cultural evolution produces tree taxonomies or classifications. However, these are often not in a format readily available for use in programs that can understand and manipulate trees. For example, the global taxonomy of languages published by the [Ethnologue](https://www.ethnologue.com/) [@Ethnologue] classifies languages into families and subgroups using a taxonomy string e.g. the language [Kalam](https://www.ethnologue.com/language/kmh) is classified as "Trans-New Guinea, Madang, Kalam-Kobon", while [Mauwake](https://www.ethnologue.com/language/mhl) is classified as "Trans-New Guinea, Madang, Croisilles, Pihom", and [Kare](https://www.ethnologue.com/language/kmf) is "Trans-New Guinea, Madang, Croisilles, Kare". This classification indicates that while all these languages are part of the Madang subgroup of the Trans-New Guinea language family, Kare and Mauwake are more closely related (as they belong to the Croisilles subgroup).

Other publications use a tabular indented format to demarcate relationships, such as this example from Stephen Wurm's classification of his proposed Yele-Solomons language phylum [@Wurm1975]:

![Example of a language taxonomy in indented format](wurm1975.png)

Both the taxonomy string and tabular format however are hard to load into software packages that can analyse, compare, visualise and manipulate trees. _TreeMaker_ aims to make this easy by converting taxonomic data into [Newick format](https://en.wikipedia.org/wiki/Newick_format) and Nexus [@Maddison1997], popular formats commonly usable by phylogenetic manipulation programs. 

## Converting a Taxonomy to a Tree:

TreeMaker can convert a text file with a taxonomy (easily obtained from Ethnologue or manually entered) like this:

```
Bilua       Yele-Solomons, Central Solomon
Baniata     Yele-Solomons, Central Solomon
Lavukaleve  Yele-Solomons, Central Solomon
Savosavo    Yele-Solomons, Central Solomon
Kazukuru    Yele-Solomons, Kazukuru
Guliguli    Yele-Solomons, Kazukuru
Dororo      Yele-Solomons, Kazukuru
Yele        Yele-Solomons
```

Into a Newick tree representation:

```
((Baniata,Bilua,Lavukaleve,Savosavo),(Dororo,Guliguli,Kazukuru),Yele)
```

...which can then be loaded into phylogenetic programs to visualise or manipulate:

![Tree visualisation of the relationships between these languages](tree.png)

TreeMaker has been used to enable the analyses in [@Bromham2018], and a number of forthcoming articles.


# References

