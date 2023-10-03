# metaip

> Find the latitude and longitude associated with an IP address..

[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![Status][status-image]][pypi-url]
[![Python Version][python-version-image]][pypi-url]
[![tests][tests-image]][tests-url]
[![Codecov][codecov-image]][codecov-url]
[![CodeQl][codeql-image]][codeql-url]
[![Docker][docker-image]][docker-url]
[![pre-commit][pre-commit-image]][pre-commit-url]
[![pre-commit.ci status][pre-commit.ci-image]][pre-commit.ci-url]
[![Imports: isort][isort-image]][isort-url]
[![Code style: black][black-image]][black-url]
[![Checked with mypy][mypy-image]][mypy-url]
[![security: bandit][bandit-image]][bandit-url]
[![Commitizen friendly][commitizen-image]][commitizen-url]
[![Conventional Commits][conventional-commits-image]][conventional-commits-url]
[![DeepSource][deepsource-image]][deepsource-url]
[![license][license-image]][license-url]
[![Pydough][pydough-image]][pydough-url]

A small command line utility that utilizes the API of ipstack to return the latitude and longitude associated with an IP address
in JSON notation.

# 🚀 Quick Start

---

## 📋 Prerequisites

---

-   [x] Python >= 3.8.
-   [x] Get an API key from [**ipstack.com**](https://ipstack.com/)

The following are optional but are recommended

-   [x] A pipx installation.

## 💾 Installation

metaip can be installed into any python environment using pip:

```bash
~ $ pip install metaip
```

However, optimal installation can be achieved using [**pipx**](https://pypa.github.io/pipx/):

```bash
~ $ pipx install metaip
```

For a development installation:

Editable (developer) installs were not possible prior to 2021, but that has been remedied by [**pep 660**](https://peps.python.org/pep-0660/).
This can be performed by either 'pip' or 'setuptools'. Clone or fork the repository first then:

```sh
$ python -m pip install -e .
```

or

```sh
$ python setup.py develop
```

## 📝 Basic Usage

Issue the command to get meta data about IP address specifying the API key

```sh
$ metaip 90.203.98.132 -k <api_key>
```

the result is return as JSON

```sh
{
    "ip": "90.203.98.132",
    "coordinates": {
        "latitude": 53.78388977050781,
        "longitude": -1.787500023841858
    }
}
```

Note: the API key is now stored for future use. More on this later.

# 📝 Usage

---

On first usage, if an API key is not specified from the command line, you will be asked to supply one:

```sh
$ metaip 90.203.98.132
Please enter your API key:
```

once the API key has benn entered, the coordinate information is returned as JSON

```shell
Please enter your API key:bb340ea1b8e683756a19d596ba421b56
{
    "ip": "90.203.98.132",
    "coordinates": {
        "latitude": 53.78388977050781,
        "longitude": -1.787500023841858
    }
}
```

Once the key has been entered once it is stored so you will not be asked for it again.

```shell
$ metaip 90.203.98.132
{
    "ip": "90.203.98.132",
    "coordinates": {
        "latitude": 53.78388977050781,
        "longitude": -1.787500023841858
    }
}
```

You can store a new key at any time by using the '-k' argument from the command line:

```shell
$>metaip 90.203.98.132 -k <api_key>
{
    "ip": "90.203.98.132",
    "coordinates": {
        "latitude": 53.78388977050781,
        "longitude": -1.787500023841858
    }
}
```

This new key will then be stored for future use.

# 🔒 Security Considerations

Obviously when dealing with API keys, the key should never be hard coded in the application.
There are a multitude of ways to deal with API keys (including using environment variables etc). To avoid hard-coding any credentials I use the Python [keyring](https://github.com/jaraco/keyring) library

Note:
On Linux, the KWallet backend relies on dbus-python, which does not always install correctly when using pip (compilation is needed). For best results, install dbus-python as a system package.
If keyring is not working then the fallback is to use the '-k' argument.

# 🧬 Design

As [**ipstack.com**](https://ipstack.com/) is a paid for service I have used the Look Before You Leap (LBYL) design principle to check Ip addresses and API keys.
This approach involves checking for preconditions or potential issues before taking an action. This is generally seen as unpythonic. However to issue malformed requests
would be wasteful on resources.
Generally speaking the Easier to Ask for Forgiveness than Permission (EAFP) is more pythonic which involves trying an action first and then handling any exceptions or errors if they occur.

# 🐳 Using Docker

## Building the Image

Start your docker runtime then:

docker build -t {{ repository }}/metaip:{{version}} .
e.g.

```shell
$ docker build -t sraking/metaip:0.1.0 -t sraking/metaip:latest .
```

Run the image (creates the container) - docker run -it {{ repository }}/metaip:{{version}} /bin/bash
e.g.

```shell
$ docker run -it sraking/metaip:0.1.0 /bin/bash
```

Upload the image to docker hub - docker push {{ repository }}/metaip:{{version}} e.g.

```shell
$ docker push sraking/metaip:0.1.0
```

## Using the ready built image

Pull the latest image from the Hub.

```bash
~ $ docker pull sraking/metaip
```

Run the image.

```bash
~ $ docker run -it sraking/metaip /bin/bash
```

Use the command line as normal in the container.

```bash
root@4d315992ca28:/app# metaip -k <api_key>
{
    "ip": "90.203.98.132",
    "coordinates": {
        "latitude": 53.78388977050781,
        "longitude": -1.787500023841858
    }
}
```

# ⚠️ Limitations

The IP addresses are restricted to IPv4 addresses.

# 📜 License

---

Distributed under the MIT license. See [![][license-image]][license-url] for more information.

<!-- Markdown link & img dfn's -->

[bandit-image]: https://img.shields.io/badge/security-bandit-yellow.svg
[bandit-url]: https://github.com/PyCQA/bandit
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[codeclimate-image]: https://api.codeclimate.com/v1/badges/7fc352185512a1dab75d/maintainability
[codeclimate-url]: https://codeclimate.com/github/Stephen-RA-King/metaip/maintainability
[codecov-image]: https://codecov.io/gh/Stephen-RA-King/metaip/branch/main/graph/badge.svg
[codecov-url]: https://app.codecov.io/gh/Stephen-RA-King/metaip
[codefactor-image]: https://www.codefactor.io/repository/github/Stephen-RA-King/metaip/badge
[codefactor-url]: https://www.codefactor.io/repository/github/Stephen-RA-King/metaip
[codeql-image]: https://github.com/Stephen-RA-King/metaip/actions/workflows/github-code-scanning/codeql/badge.svg
[codeql-url]: https://github.com/Stephen-RA-King/metaip/actions/workflows/github-code-scanning/codeql
[commitizen-image]: https://img.shields.io/badge/commitizen-friendly-brightgreen.svg
[commitizen-url]: http://commitizen.github.io/cz-cli/
[conventional-commits-image]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
[conventional-commits-url]: https://conventionalcommits.org
[deepsource-image]: https://app.deepsource.com/gh/Stephen-RA-King/metaip.svg/?label=active+issues&show_trend=true
[deepsource-url]: https://app.deepsource.com/gh/Stephen-RA-King/metaip/?ref=repository-badge
[docker-image]: https://github.com/Stephen-RA-King/metaip/actions/workflows/docker-image.yml/badge.svg
[docker-url]: https://github.com/Stephen-RA-King/metaip/actions/workflows/docker-image.yml
[downloads-image]: https://static.pepy.tech/personalized-badge/metaip?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads
[downloads-url]: https://pepy.tech/project/metaip
[format-image]: https://img.shields.io/pypi/format/metaip
[isort-image]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
[isort-url]: https://github.com/pycqa/isort/
[lgtm-alerts-image]: https://img.shields.io/lgtm/alerts/g/Stephen-RA-King/metaip.svg?logo=lgtm&logoWidth=18
[lgtm-alerts-url]: https://lgtm.com/projects/g/Stephen-RA-King/metaip/alerts/
[lgtm-quality-image]: https://img.shields.io/lgtm/grade/python/g/Stephen-RA-King/metaip.svg?logo=lgtm&logoWidth=18
[lgtm-quality-url]: https://lgtm.com/projects/g/Stephen-RA-King/metaip/context:python
[license-image]: https://img.shields.io/pypi/l/metaip
[license-url]: https://github.com/Stephen-RA-King/metaip/blob/main/LICENSE
[mypy-image]: http://www.mypy-lang.org/static/mypy_badge.svg
[mypy-url]: http://mypy-lang.org/
[pre-commit-image]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[pre-commit.ci-image]: https://results.pre-commit.ci/badge/github/Stephen-RA-King/metaip/main.svg
[pre-commit.ci-url]: https://results.pre-commit.ci/latest/github/Stephen-RA-King/metaip/main
[pydough-image]: https://img.shields.io/badge/pydough-2023-orange
[pydough-url]: https://github.com/Stephen-RA-King/pydough
[pypi-url]: https://pypi.org/project/metaip/
[pypi-image]: https://img.shields.io/pypi/v/metaip.svg
[python-version-image]: https://img.shields.io/pypi/pyversions/metaip
[readthedocs-image]: https://readthedocs.org/projects/metaip/badge/?version=latest
[readthedocs-url]: https://metaip.readthedocs.io/en/latest/?badge=latest
[status-image]: https://img.shields.io/pypi/status/metaip.svg
[tests-image]: https://github.com/Stephen-RA-King/metaip/actions/workflows/tests.yml/badge.svg
[tests-url]: https://github.com/Stephen-RA-King/metaip/actions/workflows/tests.yml
[wiki]: https://github.com/Stephen-RA-King/metaip/wiki
