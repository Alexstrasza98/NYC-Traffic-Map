# NYC-Traffic-Map

[![python versions](https://img.shields.io/badge/python-3.10.9-blue.svg)](https://www.python.org/downloads/release/python-3109/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

The final project repo for 2023 Spring ELEN 6889 Large Scale Streaming Processing at Columbia University.

## Instruction

### Create environment

```console
conda create --name=nyc-traffic python=3.10.9
conda activate nyc-traffic
pip3 install -r requirements
```

### How to run
You can run the whole process in a single script:

```console
bash run.sh
```

then start the http server

```console
http-server
```