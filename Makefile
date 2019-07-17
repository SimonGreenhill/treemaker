.PHONY: build release test clean docs

build:
	python setup.py sdist bdist_wheel

release: build
	#python setup.py sdist bdist_wheel upload
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

docs:
	sphinx-apidoc -f -o docs/source treemaker
	$(shell cd docs/; make html)

paper/paper.pdf:
	$(shell cd paper; pandoc --filter pandoc-citeproc --pdf-engine xelatex --bibliography paper.bib -f markdown paper.md -o paper.pdf)

test: clean
	py.test --cov

clean:
	rm -rf build/*

