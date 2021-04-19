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

## Master

## 1.2.0 (August 28, 2019)
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

## [1.1.0] (May 03, 2018)
### Changed
- Enhancement 1 (1.1.0)
- sub enhancement 1
- sub enhancement 2
- Enhancement 2 (1.1.0)

## [1.0.1] - May 01, 2018
### Fixed
- Bug fix 1 (1.0.1)
- sub bug 1
- sub bug 2
- Bug fix 2 (1.0.1)

## 1.0.0 (2017-01-01)
### Deprecated
- Known issue 1 (1.0.0)
- Known issue 2 (1.0.0)
"""
        )
    return changelog_file_path


def test_changelog_with_versions_and_all_categories(changelog):
    assert keepachangelog.to_dict(changelog) == {
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
            "release_date": "august 28, 2019",
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
            "release_date": "may 03, 2018",
            "version": "1.1.0",
        },
        "1.0.1": {
            "fixed": [
                "Bug fix 1 (1.0.1)",
                "sub bug 1",
                "sub bug 2",
                "Bug fix 2 (1.0.1)",
            ],
            "release_date": "may 01, 2018",
            "version": "1.0.1",
        },
        "1.0.0": {
            "deprecated": ["Known issue 1 (1.0.0)", "Known issue 2 (1.0.0)"],
            "release_date": "2017-01-01",
            "version": "1.0.0",
        },
    }


def test_changelog_with_unreleased_versions_and_all_categories(changelog):
    assert keepachangelog.to_dict(changelog, show_unreleased=True) == {
        "master": {"release_date": None, "version": "master"},
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
            "release_date": "august 28, 2019",
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
            "release_date": "may 03, 2018",
            "version": "1.1.0",
        },
        "1.0.1": {
            "fixed": [
                "Bug fix 1 (1.0.1)",
                "sub bug 1",
                "sub bug 2",
                "Bug fix 2 (1.0.1)",
            ],
            "release_date": "may 01, 2018",
            "version": "1.0.1",
        },
        "1.0.0": {
            "deprecated": ["Known issue 1 (1.0.0)", "Known issue 2 (1.0.0)"],
            "release_date": "2017-01-01",
            "version": "1.0.0",
        },
    }


def test_raw_changelog_with_versions_and_all_categories(changelog):
    assert keepachangelog.to_raw_dict(changelog) == {
        "1.2.0": {
            "raw": """### Changed
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
""",
            "release_date": "august 28, 2019",
            "version": "1.2.0",
        },
        "1.1.0": {
            "raw": """### Changed
- Enhancement 1 (1.1.0)
- sub enhancement 1
- sub enhancement 2
- Enhancement 2 (1.1.0)
""",
            "release_date": "may 03, 2018",
            "version": "1.1.0",
        },
        "1.0.1": {
            "raw": """### Fixed
- Bug fix 1 (1.0.1)
- sub bug 1
- sub bug 2
- Bug fix 2 (1.0.1)
""",
            "release_date": "may 01, 2018",
            "version": "1.0.1",
        },
        "1.0.0": {
            "raw": """### Deprecated
- Known issue 1 (1.0.0)
- Known issue 2 (1.0.0)
""",
            "release_date": "2017-01-01",
            "version": "1.0.0",
        },
    }
