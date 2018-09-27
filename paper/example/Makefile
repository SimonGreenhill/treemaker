
all: taxonomy.nwk taxonomy.nex tree.png

taxonomy.nwk: taxonomy.txt
	treemaker $< -o $@

taxonomy.nex: taxonomy.txt
	treemaker $< --mode nexus -o $@

tree.png: taxonomy.nwk
	./plot.R $< $@
	cp $@ ..

clean:
	rm -rf tree.png taxonomy.nwk taxonomy.nex
