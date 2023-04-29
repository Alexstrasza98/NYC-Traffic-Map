# NYC-Traffic-Map

[![python versions](https://img.shields.io/badge/python-3.10.9-blue.svg)](https://www.python.org/downloads/release/python-3109/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

The final project repo for 2023 Spring ELEN 6889 Large Scale Streaming Processing at Columbia University.

## Instruction

How to run:

```console
spark-submit --master "local[*]" --py-files src/congestion_model.py src/main.py
```