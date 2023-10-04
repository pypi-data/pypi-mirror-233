# Data Hand

DataHand is a collection of algorithms to read and handle data for research (e.g., Web of Science, USPTO) in Python.

DataHand allows to read a variety of typical sources used for research and convert them into a pandas DataFrame.

## Installation

To install DataHand, we recommend to use PyPI:

```
pip install datahand
```

## First steps

### 1. Read data from Web of Science

```
from datahand import read_wos

df = read_wos("file/to/path.txt")
```
