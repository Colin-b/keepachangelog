<h2 align="center">Convert changelog into dict</h2>

<p align="center">
<a href="https://pypi.org/project/keepachangelog/"><img alt="pypi version" src="https://img.shields.io/pypi/v/keepachangelog"></a>
<a href="https://travis-ci.org/Colin-b/keepachangelog"><img alt="Build status" src="https://api.travis-ci.org/Colin-b/keepachangelog.svg?branch=master"></a>
<a href="https://travis-ci.org/Colin-b/keepachangelog"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.org/Colin-b/keepachangelog"><img alt="Number of tests" src="https://img.shields.io/badge/tests-0 passed-blue"></a>
<a href="https://pypi.org/project/keepachangelog/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/keepachangelog"></a>
</p>

Convert changelog markdown file following [keep a changelog](https://keepachangelog.com/en/1.0.0/) format into python dict.

```python
import keepachangelog

# keys are the release version, values are dict containing every information, per section.
changes = keepachangelog.to_dict("CHANGELOG.md")
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install keepachangelog
```
