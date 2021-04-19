<h2 align="center">Manipulate keep a changelog files</h2>

<p align="center">
<a href="https://pypi.org/project/keepachangelog/"><img alt="pypi version" src="https://img.shields.io/pypi/v/keepachangelog"></a>
<a href="https://travis-ci.com/Colin-b/keepachangelog"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/keepachangelog.svg?branch=master"></a>
<a href="https://travis-ci.com/Colin-b/keepachangelog"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/keepachangelog"><img alt="Number of tests" src="https://img.shields.io/badge/tests-28 passed-blue"></a>
<a href="https://pypi.org/project/keepachangelog/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/keepachangelog"></a>
</p>

* [Convert to dict](#convert-changelog-to-dict)
* [Release a new version](#release)
* [Add changelog retrieval REST API endpoint](#endpoint)
  * [Starlette](#starlette)
  * [Flask-RestX](#flask-restx)

## Convert changelog to dict

Convert changelog markdown file following [keep a changelog](https://keepachangelog.com/en/1.1.0/) format into python dict.

```python
import keepachangelog

changes = keepachangelog.to_dict("path/to/CHANGELOG.md")
```

`changes` would look like:

```python
changes = {
    "1.1.0": {
        "changed": [
            "Enhancement 1 (1.1.0)",
            "sub enhancement 1",
            "sub enhancement 2",
            "Enhancement 2 (1.1.0)",
        ],
        "release_date": "2018-05-31",
        "version": "1.1.0",
    },
    "1.0.1": {
        "fixed": [
            "Bug fix 1 (1.0.1)",
            "sub bug 1",
            "sub bug 2",
            "Bug fix 2 (1.0.1)",
        ],
        "release_date": "2018-05-31",
        "version": "1.0.1",
    },
    "1.0.0": {
        "deprecated": ["Known issue 1 (1.0.0)", "Known issue 2 (1.0.0)"],
        "release_date": "2017-04-10",
        "version": "1.0.0",
    },
}
```

For a markdown file with the following content:

```markdown
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Release note 1.
- Release note 2.

### Added
- Enhancement 1
 - sub enhancement 1
 - sub enhancement 2
- Enhancement 2

### Fixed
- Bug fix 1
 - sub bug 1
 - sub bug 2
- Bug fix 2

### Security
- Known issue 1
- Known issue 2

### Deprecated
- Deprecated feature 1
- Future removal 2

### Removed
- Deprecated feature 2
- Future removal 1

## [1.1.0] - 2018-05-31
### Changed
- Enhancement 1 (1.1.0)
 - sub enhancement 1
 - sub enhancement 2
- Enhancement 2 (1.1.0)

## [1.0.1] - 2018-05-31
### Fixed
- Bug fix 1 (1.0.1)
 - sub bug 1
 - sub bug 2
- Bug fix 2 (1.0.1)

## [1.0.0] - 2017-04-10
### Deprecated
- Known issue 1 (1.0.0)
- Known issue 2 (1.0.0)

[Unreleased]: https://github.test_url/test_project/compare/v1.1.0...HEAD
[1.1.0]: https://github.test_url/test_project/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
```

`show_unreleased` parameter can be specified in order to include `Unreleased` section information.
Note that `release_date` will be set to None in such as case.

## Release

You can create a new release by using `keepachangelog.release` function.

```python
import keepachangelog

new_version = keepachangelog.release("path/to/CHANGELOG.md")
```

This will:
* Guess the new version number and return it:
  * `Removed` or `Changed` sections will be considered as breaking changes, thus incrementing the major version.
  * If the only section is `Fixed`, only patch will be incremented.
  * Otherwise, minor will be incremented.
* Update changelog.
  * Unreleased section content will be moved into a new section.
  * `[Unreleased]` link will be updated.
  * New link will be created corresponding to the new section (based on the format of the Unreleased link).

## Endpoint

### Starlette

An helper function is available to create a [starlette](https://www.starlette.io) endpoint to retrieve changelog as JSON.

```python
from starlette.applications import Starlette
from keepachangelog.starlette import add_changelog_endpoint


app = Starlette()
# /changelog endpoint will return the dict extracted from the changelog as JSON.
add_changelog_endpoint(app, "path/to/CHANGELOG.md")
```

Note: [starlette](https://pypi.python.org/pypi/starlette) module must be installed.

### Flask-RestX

An helper function is available to create a [Flask-RestX](https://flask-restx.readthedocs.io/en/latest/) endpoint to retrieve changelog as JSON.

```python
import flask
import flask_restx
from keepachangelog.flask_restx import add_changelog_endpoint


app = flask.Flask(__name__)
api = flask_restx.Api(app)
# /changelog endpoint will return the dict extracted from the changelog as JSON.
add_changelog_endpoint(api, "path/to/CHANGELOG.md")
```

Note: [flask-restx](https://pypi.python.org/pypi/flask-restx) module must be installed.

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install keepachangelog
```
