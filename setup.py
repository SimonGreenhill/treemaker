#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

VERSION = 1.01
DESCR = """
A python tool for generating a Newick formatted tree from a
list of classifications
""".replace("\n", "").strip().lstrip()

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='treemaker',
    version=VERSION,
    description=DESCR,
    long_description=long_description,
    url='https://github.com/SimonGreenhill/treemaker',
    author='Simon J. Greenhill',
    author_email='simon@simon.net.nz',
    license='BSD',
    zip_safe=True,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='phylogenetics newick taxonomy',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'treemaker = treemaker:main'
        ],
    },
    test_suite="treemaker.test_treemaker",
)
