---
title: 'treemaker:  A Python tool for constructing a Newick formatted tree from a set of classifications.'
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
date: \today
bibliography: paper.bib
---

# Summary

```treemaker``` is a Python library to convert a text-based classification schema into a Newick file for use in phylogenetic and bioinformatic programs.

Research in linguistics or cultural evolution often produces or uses tree taxonomies or classifications. However, these are usually not in a format readily available for use in programs that can understand and manipulate trees. For example, the global taxonomy of languages published by the [Ethnologue](https://www.ethnologue.com/) [@Ethnologue] classifies languages into families and subgroups using a taxonomy string e.g. the language [Kalam](https://www.ethnologue.com/language/kmh) is classified as "Trans-New Guinea, Madang, Kalam-Kobon", while [Mauwake](https://www.ethnologue.com/language/mhl) is classified as "Trans-New Guinea, Madang, Croisilles, Pihom", and [Kare](https://www.ethnologue.com/language/kmf) is "Trans-New Guinea, Madang, Croisilles, Kare". This classification indicates that while all these languages are part of the Madang subgroup of the Trans-New Guinea language family, Kare and Mauwake are more closely related (as they belong to the Croisilles subgroup).

Other publications use a tabular indented format to demarcate relationships, such as the example in Figure 1 from Stephen Wurm's classification of his proposed Yele-Solomons language phylum [@Wurm1975].

Both the taxonomy string and tabular format however are hard to load into software packages that can analyse, compare, visualise and manipulate trees. ```treemaker``` aims to make this easy by converting taxonomic data into [Newick](https://en.wikipedia.org/wiki/Newick_format) and Nexus [@Maddison1997] formats commonly used by phylogenetic manipulation programs.

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

```treemaker``` has been used to enable the analyses in [@Bromham2018], and a number of forthcoming articles.


![Example of a language taxonomy in indented format from Wurm (1975).](wurm1975.png)

![Tree visualisation of the relationships between the putative Yele-Solomons languages.](tree.png)


# References

