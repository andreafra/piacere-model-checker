# DOML Model Checker
[![Documentation Status](https://readthedocs.org/projects/piacere-model-checker/badge/?version=latest)](https://piacere-model-checker.readthedocs.io/en/latest/?badge=latest)

## Description of the component

The DOML Model Checker is a component of the [PIACERE](https://www.piacere-project.eu/) framework in charge of checking the correctness and consistency of [DOML](https://www.piacere-doml.deib.polimi.it/) models.

It consists of a web server exposing a REST API that receives a DOML model in XMI format (also called DOMLX) and provides as output a result detailing whether the model satisfies a set of internal requirements, and in case of negative results, what elements are in violation and how to fix the issue.

It also bundles a Cloud Service Provider (CSP) Compatibility tool that can provide the compatibility results of a model against common Cloud Service Providers.

## Installation

### Setup

Activate the Python Virtual Environment with:
```sh
source .venv/bin/activate
```
Install the required packages with:
```sh
pip install -r requirements.txt
```

### Run the model checker web server
```sh
python -m mc_openapi
```

### Run with Uvicorn

The project may be run with [Uvicorn](https://www.uvicorn.org/) as follows:
```sh
uvicorn --port 8080 --host 0.0.0.0 --interface wsgi --workers 2 mc_openapi.app_config:app
```
### Run tests

Run tests with:
```sh
python -m pytest
```

### Run with Docker

First, build the docker image with the usual
```sh
docker build -t wp4/dmc .
```
And then run it with
```sh
docker run -d wp4/dmc
```
The Uvicorn server will be running and listening on port `8080` of the container.
To use it locally, you may bind it with port `8080` of `localhost`
by adding `-p 127.0.0.1:8080:8080/tcp` to the `docker run` command.

## Documentation
You can read the latest version at [readthedocs.io](https://piacere-model-checker.readthedocs.io/en/latest/)

### Building the Documentation

The documentation has been written in [Sphinx](https://www.sphinx-doc.org/)
and covers both usage through the PIACERE IDE and the REST APIs.

If you want to build the documentation manually, run:
```sh
cd docs
make html
```

The documentation will be generated in `docs/_build`.

## License
This work is licensed under the Apache License 2.0.

## Contact

andrea.franchini@polimi.it

## Acknowledgement
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under Grant 
Agreement No. 101000162 (PIACERE).
