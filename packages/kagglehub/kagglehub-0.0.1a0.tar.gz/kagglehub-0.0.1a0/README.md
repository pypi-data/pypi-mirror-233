# Kaggle Hub Client Library

## Installation

Install the `kagglehub` package with pip:

```
pip install kagglehub
```

## Development

### Prequisites

We use [hatch](https://hatch.pypa.io) to manage this project.

Follow these [instructions](https://hatch.pypa.io/latest/install/) to install it.

### Tests

```
# Run all tests
hatch run tests

# Run a single test file
hatch run tests tests/test_<SOME_FILE>.py
```

### Lint / Format

```
# Lint check
hatch run lint:style
hatch run lint:typing
hatch run lint:all # for both

# Format
hatch run lint:fmt
```

### Coverage report

```
hatch cov
```

### Build

```
hatch build
```

### Publishing

This first time you publish to a repository, you will be prompted to authenticate.

```
hatch publish
```