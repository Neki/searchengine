Simple search engine
====================

[![Build Status](https://travis-ci.org/Neki/searchengine.svg?branch=master)](https://travis-ci.org/Neki/searchengine)

A very simple search engine written in Python, as part of a student project.

Caveats:
* in memory processing only
* the index is not saved to disk and computed again each time (this takes a few seconds on the CACM collection)
* generally, little attention has been given to optimizations and performance beyond using decent algorithms
* little pre-processing is done before indexing, so for instance "San Francisco" will be 2 separate tokens, singular and plurals will not be recognized as the same word...
* only a parser for the CACM collection is implemented

Three different search models are implemented (vectorial, probabilistic, and boolean).

# Installation

Requirements:
* a Python 3.4 (or better) interpreter. Previous versions of Python are not supported.
* a way to install the Python package `matplotlib`, which has native dependencies (this means having the necessary headers on your system, and a suitable compiler)

To install this tool on your system, open a terminal, go to the outer `searchengine` directory, and use
```bash
python setup.py install
```

If `matplotlib` can not be installed automatically with this command, consult the [matplotlib documentation](http://matplotlib.org/users/installing.html).

Depending on which system you are using, you may have to change the `matplotlib` backend (edit the file `matplotlibrc`). The backend used by default here has been tested on Ubuntu Linux and Windows. You will need a blocking backend. See the [matplotlib backend documentation](http://matplotlib.org/faq/usage_faq.html#what-is-a-backend) for details.

# Tests

The unit tests can be run with
```bash
python setup.py tests
```

# Usage

Once the tool has been installed, an executable named `searchengine` will be available.

Command line help:
```bash
searchengine -h
```

Perform a search:
```bash
searchengine search word
```

Evaluate the performance (precision vs recall):
```bash
searchengine -n 500 eval 0
```

See the command line help for more options and details.


# Code documentation

Some documentation is provided in form of Python docstrings ; it is assumed that the reader is already familiar with the implemented search models.
The entry point for the program is the `main` function in the file `bin/searchengine`.

