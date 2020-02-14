# Welcome <small>to Efficacy</small>

![Efficacy Logomark](../efficacy_logomark.svg)

Efficacy is the official lexer, parser, compiler, and interactive interpreter for the OcellusScript language. Efficacy can be installed as a command-line program or can be imported into Python scripts as a Python module. Efficacy currently supports Python 2.7.16 and Python 3.7+.

!!! warning "Use Python 3"
    It is highly recommended that you do not use Efficacy with Python 2.7. Support for 2.7 is included only for projects that _cannot_ be upgraded to Python 3 and is only a compatibility solution.

## Getting Started

Efficacy can be installed in a Python environment using pip:

```
pip install efficacy
```

Alternatively, Efficacy can be added as a dependency to a Poetry project:

```
poetry add efficacy; poetry update
```

## Table of Contents

1. [Usage](./01-cli.md)
2. [Module](./module/index.md)