#!/usr/bin/env Rscript
library(ape)

args <- commandArgs(trailingOnly=TRUE)
# check for -h or --help
if ((length(args) == 0) || (any(grep("^(--help|-h)$", args))))
{
    cat("usage: ./plot.R newick pdf", sep="\n")
    quit("no", 1)
}

tree <- read.tree(args[[1]])

png(args[[2]])
plot.phylo(tree, type="c", label.offset=0.1, font=1, edge.width=2)
dev.off()
