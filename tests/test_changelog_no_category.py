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

## [1.2.0] - 2018-06-01
- Release note 1.
- Release note 2.

### Fixed
- Bug fix 1
- sub bug 1
- sub bug 2
- Bug fix 2

## [1.1.0] - 2018-05-31
- Enhancement 1 (1.1.0)
- sub enhancement 1
- sub enhancement 2
- Enhancement 2 (1.1.0)

## [1.0.1] - 2018-05-31
- Bug fix 1 (1.0.1)
- sub bug 1
- sub bug 2
- Bug fix 2 (1.0.1)
"""
        )
    return changelog_file_path


def test_changelog_without_category(changelog):
    assert keepachangelog.to_dict(changelog) == {
        "1.2.0": {
            "uncategorized": ["Release note 1.", "Release note 2."],
            "fixed": ["Bug fix 1", "sub bug 1", "sub bug 2", "Bug fix 2"],
            "release_date": "2018-06-01",
            "version": "1.2.0",
            "semantic_version": {
                "buildmetadata": None,
                "major": 1,
                "minor": 2,
                "patch": 0,
                "prerelease": None,
            },
        },
        "1.1.0": {
            "uncategorized": [
                "Enhancement 1 (1.1.0)",
                "sub enhancement 1",
                "sub enhancement 2",
                "Enhancement 2 (1.1.0)",
            ],
            "release_date": "2018-05-31",
            "version": "1.1.0",
            "semantic_version": {
                "buildmetadata": None,
                "major": 1,
                "minor": 1,
                "patch": 0,
                "prerelease": None,
            },
        },
        "1.0.1": {
            "uncategorized": [
                "Bug fix 1 (1.0.1)",
                "sub bug 1",
                "sub bug 2",
                "Bug fix 2 (1.0.1)",
            ],
            "release_date": "2018-05-31",
            "version": "1.0.1",
            "semantic_version": {
                "buildmetadata": None,
                "major": 1,
                "minor": 0,
                "patch": 1,
                "prerelease": None,
            },
        },
    }
