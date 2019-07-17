import os
import unittest
from tempfile import mkdtemp
from shutil import rmtree

from treemaker import Tree, TreeMaker, parse_args

class Test_Tree(unittest.TestCase):
    
    def test_gt(self):
        assert Tree("a") < Tree("b")

    def test_lt(self):
        assert Tree("b") > Tree("a")
    
    def test_eq(self):
        assert Tree("a") == Tree("a")
    
    def test_repr(self):
        assert repr(Tree('a')) == "<Tree: a>"
    
    def test_empty_tree(self):
        assert str(Tree()) == ""
    
    def test_singleton_tree(self):
        assert str(Tree("root")) == "root"
    
    def test_simple(self):
        t = Tree('root', ['A', 'B', 'C'])
        assert str(t) == "(A,B,C)"
    
    def test_add(self):
        t = Tree('root', ['A', 'B'])
        t.add("C")
        assert str(t) == "(A,B,C)"
    
    def test_sanitise(self):
        with self.assertRaises(ValueError):
            Tree('a;', ['A', 'B'])
        
        with self.assertRaises(ValueError):
            Tree('a', ['A(', 'B'])
        
        with self.assertRaises(ValueError):
            Tree('a;', ['A', 'B)'])

    def test_recursive_add(self):
        t = Tree('root', ['A', 'B'])
        t.get("B").add("sub", ["b1", "b2"])
        assert str(t) == "(A,(b1,b2))"

    def test_get(self):
        t = Tree('root', ['A', 'B', 'C'])
        c = t.get("C")
        c.add("c1")
        c.add("c2")
        t.get("B").add('b1')
        assert str(t) == "(A,b1,(c1,c2))"
        # try from different depths
        assert t.get('c1').node == 'c1'
        assert c.get('c1').node == 'c1'

    def test_real(self):
        # yon  Trans-New Guinea, Ok-Awyu, Ok, Lowland
        # bhl  Trans-New Guinea, Ok-Awyu, Ok, Mountain
        # fai  Trans-New Guinea, Ok-Awyu, Ok, Mountain
        # yir  Trans-New Guinea, Ok-Awyu, Awyu-Dumut, Awyu
        # aax  Trans-New Guinea, Ok-Awyu, Awyu-Dumut, Dumut
        # bwp  Trans-New Guinea, Ok-Awyu, Awyu-Dumut, Dumut
        t = Tree("Ok-Awyu")
        
        Ok = t.add('Ok', ['Mountain', 'Lowland'])
        Ok.get('Lowland').add('yon')
        Ok.get('Mountain').add('bhl')
        Ok.get('Mountain').add('fai')
        
        AD = t.add('Awyu-Dumut', ['Awyu', 'Dumut'])
        AD.get('Awyu').add('yir')
        AD.get('Dumut').add('aax')
        AD.get('Dumut').add('bwp')
        assert str(t) == "((yir,(aax,bwp)),(yon,(bhl,fai)))"

    def test_is_tip(self):
        t = Tree('root', ['A', 'B'])
        t.get("B").add("sub", ["b1", "b2"])
        assert t.get("A").is_tip
        assert t.get("B").is_tip is False
        assert t.get("b1").is_tip
        assert t.get("b2").is_tip
        
    def test_is_node(self):
        t = Tree('root', ['A', 'B'])
        t.get("B").add("sub", ["b1", "b2"])
        assert t.get("A").is_node is False
        assert t.get("b1").is_node is False
        assert t.get("b2").is_node is False
    
    def test_tips(self):
        t = Tree('root', ['A', 'B'])
        t.get("B").add("sub", ["b1", "b2"])
        assert list([t.node for t in t.tips()]) == ['A', 'b1', 'b2']
    
    def test_conflicts(self):
        t = Tree('root', ['A', 'B'])
        t.get("A").add("sub", ["b1", "b2"])
        t.get("B").add("sub", ["b1", "b2"])
        assert str(t) == '((b1,b2),(b1,b2))'
    
    def test_example(self):
        t = Tree('root')
        a = t.add("family a")
        a1 = a.add("subgroup 1")
        a1.add("A1")
        
        a2 = a.add("subgroup 2")
        a2.add("A2")
        
        b = t.add("family b")
        b1 = b.add("subgroup 1")
        b1.add("B1a")
        b1.add("B1b")
        
        b2 = b.add("subgroup 2")
        b2.add("B2")
        assert str(t) == '((A1,A2),((B1a,B1b),B2))'
    
    def test_get_or_create(self):
        t = Tree('root', ['A', 'B'])
        c = t.get_or_create("C")
        c.get_or_create("c1")
        c.get_or_create("c2")
        t.get("B").add('b1')
        assert str(t) == "(A,b1,(c1,c2))"
    
    def test_deep_tree(self):
        t = Tree('root')
        taxon = t
        for i in range(0, 10):
            taxon = taxon.add(i, [i])
        assert str(t) == "(0,(1,(2,(3,(4,(5,(6,(7,(8,9)))))))))"
        


class Test_Tree_Nodelabels(unittest.TestCase):
    def test_simple(self):
        t = Tree('root', ['A', 'B', 'C'], show_nodelabels=True)
        assert str(t) == "(A,B,C)root"
    
    def test_recursive_add(self):
        t = Tree('root', ['A', 'B'], show_nodelabels=True)
        t.get("B").add("sub", ["b1", "b2"])
        assert str(t) == "(A,(b1,b2)sub)root"

    def test_real(self):
        # yon  Trans-New Guinea, Ok-Awyu, Ok, Lowland
        # bhl  Trans-New Guinea, Ok-Awyu, Ok, Mountain
        # fai  Trans-New Guinea, Ok-Awyu, Ok, Mountain
        # yir  Trans-New Guinea, Ok-Awyu, Awyu-Dumut, Awyu
        # aax  Trans-New Guinea, Ok-Awyu, Awyu-Dumut, Dumut
        # bwp  Trans-New Guinea, Ok-Awyu, Awyu-Dumut, Dumut
        t = Tree("Ok-Awyu", show_nodelabels=True)
        
        Ok = t.add('Ok', ['Mountain', 'Lowland'])
        Ok.get('Lowland').add('yon')
        Ok.get('Mountain').add('bhl')
        Ok.get('Mountain').add('fai')
        
        AD = t.add('Awyu-Dumut', ['Awyu', 'Dumut'])
        AD.get('Awyu').add('yir')
        AD.get('Dumut').add('aax')
        AD.get('Dumut').add('bwp')
        assert str(t) == "((yir,(aax,bwp)Dumut)Awyu-Dumut,(yon,(bhl,fai)Mountain)Ok)Ok-Awyu"
    
    def test_example(self):
        t = Tree('root', show_nodelabels=True)
        a = t.add("family a")
        a1 = a.add("subgroup 1")
        a1.add("A1")
        
        a2 = a.add("subgroup 2")
        a2.add("A2")
        
        b = t.add("family b")
        b1 = b.add("subgroup 1")
        b1.add("B1a")
        b1.add("B1b")
        
        b2 = b.add("subgroup 2")
        b2.add("B2")
        assert str(t) == '((A1,A2)family a,((B1a,B1b)subgroup 1,B2)family b)root'
    
    def test_deep_tree(self):
        t = Tree('root', show_nodelabels=True)
        taxon = t
        for i in range(0, 10):
            taxon = taxon.add(i, [i])
        assert str(t) == "(0,(1,(2,(3,(4,(5,(6,(7,(8,9)8)7)6)5)4)3)2)1)0"


class Test_TreeMaker(unittest.TestCase):
    def test_error_on_bad_taxon(self):
        t = TreeMaker()
        with self.assertRaises(ValueError):
            t.add('A (x)', 'a')
        with self.assertRaises(ValueError):
            t.add('A)', 'a')
        with self.assertRaises(ValueError):
            t.add('A(', 'a')
        
    def test_parse_classification(self):
        t = TreeMaker()
        assert t.parse_classification("a, b, c") == ['a', 'b', 'c']
        assert t.parse_classification("family a, subgroup 1") == [
            'family a', 'subgroup 1'
        ]
    
    def test_add(self):
        t = TreeMaker()
        t.add('A', 'a')
        t.add('AB1', 'a, b')
        t.add('AB2', 'a, b')
        t.add('C', 'c')
        assert str(t.tree) == "((A,(AB1,AB2)),C)"
    
    def test_add_2(self):
        t = TreeMaker()
        t.add('A1', 'family a, subgroup 1')
        t.add('A2', 'family a, subgroup 2')
        t.add('B1a', 'family b, subgroup 1')
        t.add('B1b', 'family b, subgroup 1')
        t.add('B2', 'family b, subgroup 2')
        assert str(t.tree) == "((A1,A2),((B1a,B1b),B2))"
    
    def test_add_from(self):
        taxa = [
            ('A1', 'family a, subgroup 1'),
            ('A2', 'family a, subgroup 2'),
            ('B1a', 'family b, subgroup 1'),
            ('B1b', 'family b, subgroup 1'),
            ('B2', 'family b, subgroup 2'),
        ]
        t = TreeMaker()
        t.add_from(taxa)
        assert str(t.tree) == "((A1,A2),((B1a,B1b),B2))"
    
    def test_add_from_exception(self):
        taxa = [
            ('A1', 'family a, subgroup 1'),
            ('A2family a, subgroup 2'),  # oops.
            ('B1a', 'family b, subgroup 1'),
        ]
        with self.assertRaises(ValueError):
            t = TreeMaker().add_from(taxa)

    def test_error_on_duplicate(self):
        t = TreeMaker()
        t.add('A', 'a')
        with self.assertRaises(ValueError):
            t.add('A', 'a')


class Test_TreeMakerIO(unittest.TestCase):
    """
    Test the IO functionality of TreeMaker in its own test class as we need
    some setup/teardown logic.
    """
    
    @classmethod
    def setUpClass(cls):
        cls.t = TreeMaker()
        cls.t.add('A', 'a')
        cls.t.add('AB1', 'a, b')
        cls.t.add('AB2', 'a, b')
        cls.t.add('C', 'c')
        
        cls.tmpdir = mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        if cls.tmpdir and os.path.isdir(cls.tmpdir):
            rmtree(cls.tmpdir)
    
    def test_write_newick(self):
        assert self.t.write(mode="newick") == "((A,(AB1,AB2)),C);"

    def test_write_nexus(self):
        assert self.t.write(mode="nexus").startswith("#NEXUS")
        assert "((A,(AB1,AB2)),C)" in self.t.write(mode="nexus")
    
    def test_write_nexus_error_on_bad_method(self):
        with self.assertRaises(ValueError):
            self.t.write(mode="banana")
    
    def test_write_to_file_error_on_invalid_mode(self):
        outfile = os.path.join(self.tmpdir, 'out1')
        with self.assertRaises(ValueError):
            self.t.write_to_file(outfile, mode="a")
    
    def test_write_to_file_error_on_existing_file(self):
        outfile = os.path.join(self.tmpdir, 'out2')
        # create
        with open(outfile, 'w') as handle:
            handle.write('important data')
        
        with self.assertRaises(IOError):
            self.t.write_to_file(outfile)
    
    def test_write_to_nexus(self):
        outfile = os.path.join(self.tmpdir, 'out.nex')
        self.t.write_to_file(outfile, mode="nexus")
        with open(outfile, 'r') as handle:
            content = handle.read().strip()
        assert content.startswith("#NEXUS")
            
    def test_write_to_newick(self):
        outfile = os.path.join(self.tmpdir, 'out.nwk')
        self.t.write_to_file(outfile, mode="newick")
        with open(outfile, 'r') as handle:
            content = handle.read()
        assert str(self.t.tree) in content
    
    def test_read(self):
        outfile = os.path.join(self.tmpdir, 'read.txt')
        with open(outfile, 'w') as handle:
            handle.write('A         a\n')
            handle.write('AB1       a, b\n')
            handle.write('AB2       a, b\n')
            handle.write('C         c\n')
        t = TreeMaker()
        t.read(outfile)
        assert str(self.t.tree) == str(t.tree)

    def test_read_with_tabs(self):
        outfile = os.path.join(self.tmpdir, 'read.txt')
        with open(outfile, 'w') as handle:
            handle.write('A\ta\n')
            handle.write('AB1\ta, b\n')
            handle.write('AB2\ta, b\n')
            handle.write('C\tc\n')
        t = TreeMaker()
        t.read(outfile)
        assert str(self.t.tree) == str(t.tree)

    def test_read_error_on_malformed(self):
        outfile = os.path.join(self.tmpdir, 'read-error.txt')
        with open(outfile, 'w') as handle:
            handle.write('Aasasd\n')
        t = TreeMaker()
        with self.assertRaises(ValueError):
            t.read(outfile)

    def test_read_skips_empty_lines(self):
        outfile = os.path.join(self.tmpdir, 'read-empty.txt')
        with open(outfile, 'w') as handle:
            handle.write('A         a\n')
            handle.write('\n')
            handle.write('\n')
            handle.write('B         b\n')
        t = TreeMaker()
        t.read(outfile)
        assert str(t.tree) == '(A,B)'


class Test_ParseArgs(unittest.TestCase):
    def test_IOError_on_no_file(self):
        with self.assertRaises(IOError):
            parse_args(['a'])
    
    def test_parse_filename_only(self):
        i, m, o, n = parse_args(['%s' % __file__])
        assert i == __file__
        assert m == 'newick'  # default
        assert o is None  # No output file
        assert n == False  # default

    def test_parse_filename_and_output(self):
        i, m, o, n = parse_args(['%s' % __file__, '-o', 'test'])
        assert i == __file__
        assert m == 'newick'  # default
        assert o == 'test', repr(o)
        assert n == False  # default

    def test_parse_filename_and_full_output(self):
        i, m, o, n = parse_args(['%s' % __file__, '--output', 'test'])
        assert i == __file__
        assert m == 'newick'  # default
        assert o == 'test', repr(o)
        assert n == False  # default

    def test_parse_mode(self):
        i, m, o, n = parse_args(['%s' % __file__, '-m' , 'newick'])
        assert i == __file__
        assert m == 'newick'
        assert n == False  # default
        
        i, m, o, n = parse_args(['%s' % __file__, '-m', 'nexus'])
        assert i == __file__
        assert m == 'nexus'
        assert n == False  # default

    def test_parse_nodelabels(self):
        i, m, o, n = parse_args(['%s' % __file__, '-l'])
        assert i == __file__
        assert m == 'newick'  # default
        assert n == True


if __name__ == '__main__':
    unittest.main()
