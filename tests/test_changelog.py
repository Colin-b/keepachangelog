import io
import os
import os.path

import pytest

import keepachangelog

changelog_dict = {
        "1.2.0": {
            "added": [
                "Enhancement 1",
                "sub enhancement 1",
                "sub enhancement 2",
                "Enhancement 2",
            ],
            "changed": ["Release note 1.", "Release note 2."],
            "deprecated": ["Deprecated feature 1", "Future removal 2"],
            "fixed": ["Bug fix 1", "sub bug 1", "sub bug 2", "Bug fix 2"],
            "release_date": "2018-06-01",
            "removed": ["Deprecated feature 2", "Future removal 1"],
            "security": ["Known issue 1", "Known issue 2"],
            "version": "1.2.0",
        },
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

## [1.2.0] - 2018-06-01
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
    return changelog_file_path


def test_changelog_with_versions_and_all_categories(changelog):
    assert keepachangelog.to_dict(changelog) == changelog_dict

def test_changelog_with_versions_and_all_categories_iobase(changelog):

    buffer = io.StringIO(open(changelog).read())

    assert keepachangelog.to_dict(buffer) == changelog_dict

    with pytest.raises(AssertionError):
        assert keepachangelog.to_dict(buffer) == changelog_dict

    buffer.seek(0)
    assert keepachangelog.to_dict(buffer) == changelog_dict
