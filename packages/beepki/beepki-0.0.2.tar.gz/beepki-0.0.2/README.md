# beep

A simple module for making signal when exiting from a block

## Installation

### From PyPI

Install the package with `pip` using the following command:

```sh
pip install beepki
```

### From GitHub

Alternatively, the most recent version of the tool can be pulled directly from this repo:

```sh
pip install git+https://github.com/zeionara/beep
```

## Usage

```py
with beep():
    raise ValueError('What are the beepki after all?')
```
