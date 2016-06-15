.PHONY: build release test clean

build:
	python setup.py sdist bdist_wheel

release:
	python setup.py sdist bdist_wheel upload

test: clean
	py.test --cov

clean:
	rm -rf build/*

