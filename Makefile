.PHONY: build release test clean docs

build:
	python setup.py sdist bdist_wheel

release:
	python setup.py sdist bdist_wheel upload

docs:
	sphinx-apidoc -f -o docs/source treemaker
	cd docs/; make html; cd ..

test: clean
	py.test --cov

clean:
	rm -rf build/*

