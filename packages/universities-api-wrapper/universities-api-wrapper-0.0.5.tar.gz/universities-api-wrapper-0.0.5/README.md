# Universities API Wrapper
![Build](https://github.com/jremes-foss/universities-api-wrapper/actions/workflows/ci.yml/badge.svg?branch=main)
[![Downloads](https://static.pepy.tech/badge/universities-api-wrapper)](https://pepy.tech/project/universities-api-wrapper)

This is a small API wrapper designed to consume [Universities API](https://github.com/Hipo/university-domains-list-api) by [Hipo](http://hipolabs.com/). from Python command line. API consumer was built as a project to build first Python library.

## Requirements

This package requires [requests](https://pypi.org/project/requests/) package to function properly.

## Installation

### Local installation

Install the package via:

```bash
python setup.py install
```

### Docker installation

GitHub repository includes Dockerfile for testing on local box.

Build Docker image with following command:

```bash
docker build .
```

This builds the Docker image. Next, you can run the image in container:

```bash
docker exec -it CONTAINER_ID bash
```

This will land you in a shell in Docker container which allows you to use the library for testing purposes.

### PyPI installation

Alternatively, you can install package via PyPI `pip` package manager.

```bash
pip install universities-api-wrapper
```

## Usage

Once installed, you can use wrapper the following way. First, instantiate the library.

```python
from universities_api_wrapper import HipolabsUniversitiesAPI
```

Then initialize the client. If you are using local connection only:

```python
client = HipolabsUniversitiesAPI("local")
```

By default, local connector is attempting to connect port `8080/tcp`.

Alternatively, if you wish to use remote connection:

```python
client = HipolabsUniversitiesAPI("remote")
```

If you wish to use alternative port, for example, `8888/tcp`, you can invoke connector like this:

```python
client = HipolabsUniversitiesAPI("remote", 8888)
```

If you pass anything else, library will raise `UniversitiesAPIError`.

Client has now been initialized. Let's start searching.

### Search by Country

```python
client.search("Turkey")
```

### Search by University

```python
client.search(None, "East")
```

### Combination Search

This function is searching by country and university name.

```python
client.search("Turkey", "East")
```

### Filters

You can filter elements of the search results via `filter` parameter in `search` function. For example, to return only university names you can use the following:

```python
client.search("Turkey", "Ankara", "names")
```

To filter websites, use `websites` filter:

```python
client.search("Turkey", "Ankara", "websites")
```

To filter domains, use `domains` filter:

```python
client.search("Turkey", "Ankara", "domains")
```

Please note: Domain filter will return list which elements are lists.

## Unit Tests and Continuous Integration

This module has built-in unit test kit in `tests` folder. You can run the unit tests by:

```
python -m pytest tests
```

This module uses Continuous Integration with [GitHub Actions](https://docs.github.com/en/actions). Pipeline is designed to run automated unit tests as part of Continuous Integration pipeline.

## License

This API consumer is licensed under [MIT license](https://opensource.org/license/mit/).
