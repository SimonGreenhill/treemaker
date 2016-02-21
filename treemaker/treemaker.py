#!/usr/bin/env python
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import os
import codecs

VERSION = "1.0"

NEXUS_TEMPLATE = """#NEXUS

begin trees;
   tree %(label)s = %(tree)s;
end;
"""



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
            if child.is_node:
                yield from self.tips(child)
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
    
    def add(self, leaf, classification):
        """
        Adds `leaf` to the tree in the location specified by `classification`
        """
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
        Adds all entries from an `iterable`. `iterable` should be a list of lists
        or a list of tuples (etc) with 2 values - the first one the taxon name, the
        second the classification string, e.g. 
        
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
                if ' ' not in line:
                    raise ValueError("Malformed line %d -- I need one space: %s" % (i, line))
                self.add(*[_.strip() for _ in line.split(" ", 1)])
        return self.tree
    
    def write(self):
        return str(self.tree)
        
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
            content = NEXUS_TEMPLATE % {
                'label': self.tree.node if len(self.tree.node) else 'tree',
                'tree': str(self.tree),
            }
        elif mode == 'newick':
            content = str(self.tree)
        else:
            raise ValueError("Unknown output mode. Please use 'nexus' or 'newick'")
        
        with codecs.open(filename, 'w') as handle:
            handle.write(content)
        