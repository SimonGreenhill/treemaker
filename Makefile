.PHONY: build release test clean docs

build:
	python setup.py sdist bdist_wheel

release:
	python setup.py sdist bdist_wheel upload

docs:
	sphinx-apidoc -f -o docs/source treemaker
	$(shell cd docs/; make html)

paper/paper.pdf:
	$(shell cd paper; pandoc --filter pandoc-citeproc --pdf-engine xelatex --bibliography paper.bib -f markdown paper.md -o paper.pdf)

test: clean
	py.test --cov

clean:
	rm -rf build/*

