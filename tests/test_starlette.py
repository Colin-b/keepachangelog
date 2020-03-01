import os

from starlette.applications import Starlette
from starlette.testclient import TestClient

from keepachangelog.starlette import add_changelog_endpoint


def test_changelog_endpoint_with_file(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
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
"""
        )

    app = Starlette()
    add_changelog_endpoint(app, changelog_file_path)
    with TestClient(app) as client:
        response = client.get("/changelog")
        assert response.status_code == 200
        assert response.json() == {
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


def test_changelog_endpoint_without_file():
    app = Starlette()
    add_changelog_endpoint(app, "non existing")
    with TestClient(app) as client:
        response = client.get("/changelog")
        assert response.status_code == 200
        assert response.json() == {}
