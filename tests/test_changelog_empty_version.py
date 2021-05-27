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

## [] - 2018-06-01
### Changed
- Release note 1.
- Release note 2.

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
"""
        )
    return changelog_file_path


def test_changelog_with_empty_version(changelog):
    assert keepachangelog.to_dict(changelog) == {
        "": {
            "changed": ["Release note 1.", "Release note 2."],
            "deprecated": ["Deprecated feature 1", "Future removal 2"],
            "fixed": ["Bug fix 1", "sub bug 1", "sub bug 2", "Bug fix 2"],
            "removed": ["Deprecated feature 2", "Future removal 1"],
            "security": ["Known issue 1", "Known issue 2"],
            "metadata": {
                "release_date": "2018-06-01",
                "version": "",
                "semantic_version": {
                    "buildmetadata": None,
                    "major": 0,
                    "minor": 0,
                    "patch": 0,
                    "prerelease": None,
                },
            },
        },
    }
