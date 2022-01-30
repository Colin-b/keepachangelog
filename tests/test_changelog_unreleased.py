import os
import os.path

import pytest

import keepachangelog


@pytest.fixture
def changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Release note 0. 
### Changed
- Release note 1. 
* Release note 2.

### Added
- Enhancement 1
 - sub enhancement 1 
 * sub enhancement 2
- Enhancement 2

### Fixed
- Bug fix 1
 - sub bug 1
 * sub bug 2
- Bug fix 2

### Security
* Known issue 1
- Known issue 2

### Deprecated
- Deprecated feature 1 
* Future removal 2

### Removed
- Deprecated feature 2
* Future removal 1 

## [1.1.0] - 2018-05-31
### Changed
- Enhancement 1 (1.1.0)
- sub *enhancement 1*
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

## [0.0.1] - 2017-01-01
### Added
- First release

[Unreleased]: https://github.test_url/test_project/compare/v1.1.0...HEAD
[1.1.0]: https://github.test_url/test_project/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.test_url/test_project/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
"""
        )
    return changelog_file_path


def test_changelog_with_versions_and_all_categories(changelog):
    assert keepachangelog.to_dict(changelog, show_unreleased=True) == {
        "unreleased": {
            "changed": ["Release note 1.", "Release note 2."],
            "added": [
                "Enhancement 1",
                "sub enhancement 1",
                "sub enhancement 2",
                "Enhancement 2",
            ],
            "fixed": ["Bug fix 1", "sub bug 1", "sub bug 2", "Bug fix 2"],
            "security": ["Known issue 1", "Known issue 2"],
            "uncategorized": ["Release note 0."],
            "deprecated": ["Deprecated feature 1", "Future removal 2"],
            "removed": ["Deprecated feature 2", "Future removal 1"],
            "metadata": {
                "version": "unreleased",
                "release_date": None,
                "url": "https://github.test_url/test_project/compare/v1.1.0...HEAD",
            },
        },
        "1.1.0": {
            "changed": [
                "Enhancement 1 (1.1.0)",
                "sub *enhancement 1*",
                "sub enhancement 2",
                "Enhancement 2 (1.1.0)",
            ],
            "metadata": {
                "version": "1.1.0",
                "semantic_version": {
                    "buildmetadata": None,
                    "major": 1,
                    "minor": 1,
                    "patch": 0,
                    "prerelease": None,
                },
                "release_date": "2018-05-31",
                "url": "https://github.test_url/test_project/compare/v1.0.2...v1.1.0",
            },
        },
        "1.0.2": {
            "metadata": {
                "url": "https://github.test_url/test_project/compare/v1.0.1...v1.0.2",
                "version": "1.0.2",
                "semantic_version": {
                    "buildmetadata": None,
                    "major": 1,
                    "minor": 0,
                    "patch": 2,
                    "prerelease": None,
                },
            },
        },
        "1.0.1": {
            "fixed": [
                "Bug fix 1 (1.0.1)",
                "sub bug 1",
                "sub bug 2",
                "Bug fix 2 (1.0.1)",
            ],
            "metadata": {
                "version": "1.0.1",
                "semantic_version": {
                    "buildmetadata": None,
                    "major": 1,
                    "minor": 0,
                    "patch": 1,
                    "prerelease": None,
                },
                "release_date": "2018-05-31",
                "url": "https://github.test_url/test_project/compare/v1.0.0...v1.0.1",
            },
        },
        "1.0.0": {
            "deprecated": ["Known issue 1 (1.0.0)", "Known issue 2 (1.0.0)"],
            "metadata": {
                "version": "1.0.0",
                "semantic_version": {
                    "buildmetadata": None,
                    "major": 1,
                    "minor": 0,
                    "patch": 0,
                    "prerelease": None,
                },
                "release_date": "2017-04-10",
                "url": "https://github.test_url/test_project/releases/tag/v1.0.0",
            },
        },
        "0.0.1": {
            "added": ["First release"],
            "metadata": {
                "release_date": "2017-01-01",
                "semantic_version": {
                    "buildmetadata": None,
                    "major": 0,
                    "minor": 0,
                    "patch": 1,
                    "prerelease": None,
                },
                "version": "0.0.1",
            },
        },
    }


def test_changelog_from_dict(changelog):
    releases = keepachangelog.to_dict(changelog, show_unreleased=True)

    assert (
        keepachangelog.from_dict(releases)
        == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Release note 0.

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
- sub *enhancement 1*
- sub enhancement 2
- Enhancement 2 (1.1.0)

## [1.0.2]
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

## [0.0.1] - 2017-01-01
### Added
- First release

[Unreleased]: https://github.test_url/test_project/compare/v1.1.0...HEAD
[1.1.0]: https://github.test_url/test_project/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.test_url/test_project/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
"""
    )
