#!/usr/bin/env python
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import os
import re
import sys
import codecs
import argparse

VERSION = "1.0"

NEXUS_TEMPLATE = """#NEXUS

begin trees;
   tree %(label)s = %(tree)s;
end;
"""

IS_WHITESPACE = re.compile(r"""\s+""")


class Tree(object):
    def __init__(self, node=None, children=None):
        self.children = []
        
        if node is None:
            self.node = ''
        else:
            self.node = str(node)
        
        if children is not None:
            [self.add(child) for child in children]
    
    def __lt__(self, other):
        return self.node < other.node
        
    def __gt__(self, other):
        return self.node > other.node
    
    def __eq__(self, other):
        return self.node == other.node
    
    @property
    def is_tip(self):
        """Returns True if node is a tip"""
        return len(self.children) == 0
    
    @property
    def is_node(self):
        """Returns True if node is a node (i.e. has children)"""
        return len(self.children) > 0
    
    def add(self, node, children=None):
        """Adds a node (with optional children) to the tree"""
        if not isinstance(node, Tree):
            node = Tree(node, children)
        self.children.append(node)
        return node
    
    def get_or_create(self, label):
        """Helper function to get or create a node"""
        found = self.get(label)
        if found:
            return found
        else:
            return self.add(label)
    
    def get(self, label, node=None):
        """Searches tree for node `label`"""
        node = self if node is None else node
        for child in node.children:
            if child.node == label:
                return child
            else:
                found = self.get(label, child)
                if found:
                    return found
        return None
    
    def tips(self, node=None):
        """Returns a list of the tips in the tree"""
        node = self if node is None else node
        for child in node.children:
            if child.is_node:  # remove yield from so we can support py2.7
                for n in self.tips(child):
                    yield n
            if child.is_tip:
                yield child
    
    def __repr__(self):
        return "<Tree: %s>" % self.node
    
    def __str__(self):
        if len(self.children) == 0:
            return self.node
        else:
            out = ",".join([str(c) for c in sorted(self.children)])
            if len(self.children) == 1:
                return out
            else:
                return "(%s)" % out


class TreeMaker(object):
    def __init__(self, label="root"):
        self.tree = Tree(label)
        self._added = set()
    
    def _check_taxon(self, taxon):
        for char in "()":
            if char in taxon:
                raise ValueError("Error: %s is not allowed in taxon names" % char)
    
    def add(self, leaf, classification):
        """
        Adds `leaf` to the tree in the location specified by `classification`
        """
        self._check_taxon(leaf)
        if (leaf, classification) in self._added:
            raise ValueError("Duplicate Taxon/Classification")
        
        parent = self.tree
        for node in self.parse_classification(classification):
            parent = parent.get_or_create(node)
        parent.add(leaf)
        self._added.add((leaf, classification))
        return self.tree
    
    def add_from(self, iterable):
        """
        Adds all entries from an `iterable`. `iterable` should be a list of
        lists or a list of tuples (etc) with 2 values - the first one the taxon
        name, the second the classification string, e.g.
        
        >>> iterable = [
        >>>     ['taxon1', 'a, a'],
        >>>     ['taxon2', 'a, b'],
        >>> ]
        >>> tree = TreeMaker().add_from(iterable)
        
        """
        for i, row in enumerate(iterable, 1):
            assert len(row) == 2, "entry %d is not a tuple or list" % i
            self.add(row[0], row[1])
        return self.tree
        
    def parse_classification(self, classification):
        """
        Parses a classification string into nodes
        """
        # simple for now, but easily subclassed for more complicated schema
        return [node.strip() for node in classification.strip().split(",")]
    
    def read(self, filename):
        with codecs.open(filename, 'r', encoding="utf8") as handle:
            for i, line in enumerate(handle, 1):
                line = line.strip()
                if len(line) == 0:
                    continue  # skip empty lines
                
                if IS_WHITESPACE.findall(line) is None:
                    raise ValueError(
                        "Malformed line %d -- I need one space: %s" % (i, line)
                    )
                line = [_.strip() for _ in IS_WHITESPACE.split(line, 1)]
                if len(line) != 2:
                    raise ValueError("Malformed line %d: %s" % (i, line))
                self.add(*line)
        return self.tree
    
    def write(self, mode="newick"):
        """
        Writes the output form of the tree.
        
        `mode`:
            "nexus" = a nexus file is generated
            "newick" = a newick file (bare tree) is generated
        
        Raises ValueError if mode is not "nexus" or "newick".
        """
        if mode == 'newick':
            return str(self.tree)
        elif mode == 'nexus':
            return NEXUS_TEMPLATE % {
                'label': self.tree.node if len(self.tree.node) else 'tree',
                'tree': str(self.tree),
            }
        else:
            raise ValueError(
                "Unknown output mode. Please use 'nexus' or 'newick'"
            )
        
    def write_to_file(self, filename, mode="nexus"):
        """
        Writes the tree to `filename`.
        
        `mode`:
            "nexus" = a nexus file is generated
            "newick" = a newick file (bare tree) is generated
        
        Raises IOError if `filename` already exists.
        Raises ValueError if mode is not "nexus" or "newick".
        """
        if os.path.isfile(filename):
            raise IOError("File %s already exists" % filename)
        
        if mode == 'nexus':
            content = self.write(mode="nexus")
        elif mode == 'newick':
            content = self.write(mode="newick")
        else:
            raise ValueError(
                "Unknown output mode. Please use 'nexus' or 'newick'"
            )
        
        with codecs.open(filename, 'w') as handle:
            handle.write(content)


def parse_args(args):
    """
    Parses command line arguments

    Returns a tuple of (inputfile, method, outputfile)
    """
    descr = 'Constructs a tree from a classification table'
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument("input", help="inputfile")
    parser.add_argument(
        '-o', "--output", dest='output', default=None,
        help="output file", action='store'
    )
    parser.add_argument(
        '-m', "--mode", dest='mode', choices=['nexus', 'newick'], default="newick",
        help="output mode: nexus or newick", action='store'
    )
    args = parser.parse_args(args)
    
    if not os.path.isfile(args.input):
        raise IOError("File %s does not exist" % args.input)
    
    return (args.input, args.mode, args.output)


def main(args=None):  # pragma: no cover
    if args is None:
        args = sys.argv[1:]
    infile, mode, outfile = parse_args(args)
    t = TreeMaker()
    t.read(infile)
    
    if outfile is None:
        print(t.write(mode=mode))
    else:
        t.write_to_file(outfile, mode=mode)
