#!/usr/bin/env python
#coding=utf-8
"""TreeMaker"""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2018 Simon J. Greenhill'
__license__ = 'New-style BSD'

import os
import re
import sys
import codecs
import argparse
from functools import total_ordering

VERSION = "1.3"

NEXUS_TEMPLATE = """#NEXUS

begin trees;
   tree %(label)s = %(tree)s
end;
"""

BADCHARS = "();"

IS_WHITESPACE = re.compile(r"""\s+""")


@total_ordering
class Tree(object):
    """
    Tree object to represent the classification taxonomy.

    Args:
        node (str): Label for this node.
        children (list): Optional list of children nodes
        show_nodelabels (boolean): A flag to show nodelabels or not (default=False)
    """
    def __init__(self, node=None, children=None, show_nodelabels=False):
        self.children = []
        self.show_nodelabels = show_nodelabels
        if node is None:
            self.node = ''
        else:
            self.node = self._sanitise(str(node))
        
        if children is not None:
            [self.add(child) for child in children]
    
    def __lt__(self, other):
        return self.node < other.node
    
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
        """
        Adds a node (with optional children) to the tree.

        Args:
            node (str): Label for this node.
            children (list): Optional list of children nodes

        Returns:
            treemaker.Tree: the created node matching `label`.
        """
        if not isinstance(node, Tree):
            node = Tree(node, children, show_nodelabels=self.show_nodelabels)
        self._sanitise(node.node)
        self.children.append(node)
        return node
    
    def get_or_create(self, label):
        """
        Helper function to get or create a node.

        Args:
            label (str): Label for this node.

        Returns:
            treemaker.Tree: the found or created node matching `label`.
        """
        found = self.get(label)
        if found:
            return found
        return self.add(label)
    
    def get(self, label, node=None):
        """
        Searches tree for node `label`.

        Args:
            label (str): Label for this node.
            node (treemaker.Tree): (optional) parent node.
                Default is current node.

        Returns:
            treemaker.Tree: the found or created node matching `label`.
        """
        node = self if node is None else node
        for child in node.children:
            if child.node == label:
                return child
            found = self.get(label, child)
            if found:
                return found
        return None
    
    def tips(self, node=None):
        """
        Returns a list of the tips in the tree

        Args:
            node (treemaker.Tree): (optional) parent node. Default is current 
                node.

        Returns:
            List[treemaker.Tree]: the tip nodes from the given node.
        """
        node = self if node is None else node
        for child in node.children:
            if child.is_node:  # remove yield from so we can support py2.7
                for n in self.tips(child):
                    yield n
            if child.is_tip:
                yield child
    
    def _sanitise(self, node):
        for char in BADCHARS:
            if char in node:
                raise ValueError(
                    "Forbidden character '%s' node: %s" % (char, node)
                )
        return node

    def __repr__(self):
        return "<Tree: %s>" % self.node
    
    def __str__(self):
        if not self.children:
            return self.node
        else:
            out = ",".join([str(c) for c in sorted(self.children)])
            if len(self.children) == 1:
                return out
            elif self.show_nodelabels:
                return "(%s)%s" % (out, self.node)
            else:
                return "(%s)" % out


class TreeMaker(object):
    def __init__(self, label="root", nodelabels=False):
        self.tree = Tree(label, show_nodelabels=nodelabels)
        self._added = set()
    
    def _check_taxon(self, taxon):
        for char in "()":
            if char in taxon:
                raise ValueError(
                    "Error: %s is not allowed in taxon names" % char
                )
    
    def add(self, leaf, classification):
        """
        Adds `leaf` to the tree in the location specified by `classification`

        Args:
            leaf (str): Leaf label
            classification (str): A classification string of a format handled
                by `parse_classification`.

        Returns:
            treemaker.Tree: the tree with the new node added.

        Raises:
            ValueError: If a duplicate leaf label or classification is given.
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

        Args:
            iterable (iter): an iterable (e.g. a list).

        Returns:
            treemaker.Tree: the tree with the new nodes added.

        Raises:
            ValueError: If each member of the iterable does not contain two 
                entries (leaf name, and classification).
        """
        for i, row in enumerate(iterable, 1):
            if len(row) != 2:
                raise ValueError("entry %d is not a tuple or list" % i)
            self.add(row[0], row[1])
        return self.tree
        
    def parse_classification(self, classification):
        """
        Parses a classification string into nodes.

        >>> Tree().parse_classification("Indo-European, Germanic, English")
        >>> ["Indo-European", "Germanic", "English"]

        Args:
            classification (str): a classification string e.g.
                "clade 1, clade 2, clade 3"

        Returns:
            List: a list of the classification nodes.
        """
        # simple for now, but easily subclassed for more complicated schema
        return [node.strip() for node in classification.strip().split(",")]
    
    def read(self, filename):
        """
        Reads data from `filename` and constructs a tree.
        
        `filename` should be formatted as follows::

            Taxon1   FamilyA, GroupA, SubgroupA
            Taxon2   FamilyA, GroupA, SubgroupB
            Taxon3   FamilyA, GroupB
            ... etc

        Args:
            filename (str): a filename containing the classification.

        Returns:
            treemaker.Tree: a `Tree` with the specified classification.

        Raises:
            ValueError: if a line in the file is not able to be parsed.
        """
        with codecs.open(filename, 'r', encoding="utf8") as handle:
            for i, line in enumerate(handle, 1):
                line = line.strip()
                if not line:
                    continue  # skip empty lines
                
                if not IS_WHITESPACE.findall(line):
                    raise ValueError(
                        "Malformed line %d -- I need one space: %s" % (i, line)
                    )
                self.add(*[_.strip() for _ in IS_WHITESPACE.split(line, 1)])
        return self.tree
    
    def write(self, mode="newick"):
        """
        Writes the output form of the tree.
        
        Args:
            mode (str): An output mode. One of: 
                * "nexus" = a nexus file is generated
                * "newick" = a newick file (bare tree) is generated
            nodelabels (bool): show nodelabels or not (default False)

        Returns:
            str: a string containing the formatted content.
        
        Raises:
            ValueError: if mode is not "nexus" or "newick".
        """
        if mode == 'newick':
            return "%s;" % str(self.tree)
        elif mode == 'nexus':
            return NEXUS_TEMPLATE % {
                'label': self.tree.node if self.tree.node else 'tree',
                'tree': str(self.tree),
            }
        else:
            raise ValueError(
                "Unknown output mode. Please use 'nexus' or 'newick'"
            )
        
    def write_to_file(self, filename, mode="nexus"):
        """
        Writes the tree to `filename`.
        

        Args:
            mode (str): An output mode. One of:
                * "nexus" = a nexus file is generated
                * "newick" = a newick file (bare tree) is generated
            nodelabels (bool): show nodelabels or not (default False)
        
        Returns:
            None

        Raises:
            IOError: if `filename` already exists.
            ValueError: if mode is not "nexus" or "newick".
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
    parser.add_argument(
        '-l', "--labels", dest='nodelabels', default=False,
        help="show node labels", action='store_true'
    )
    args = parser.parse_args(args)
    
    if not os.path.isfile(args.input):
        raise IOError("File %s does not exist" % args.input)
    
    return (args.input, args.mode, args.output, args.nodelabels)


def main(args=None):  # pragma: no cover
    if args is None:
        args = sys.argv[1:]
    infile, mode, outfile, nodelabels = parse_args(args)
    t = TreeMaker(nodelabels=nodelabels)
    t.read(infile)
    if outfile is None:
        print(t.write(mode=mode))
    else:
        t.write_to_file(outfile, mode=mode)
