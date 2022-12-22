import keepachangelog


changelog_as_text = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2018-06-01
### Added
- Enhancement 1
- sub enhancement 1
- sub enhancement 2
- Enhancement 2

### Changed
- Release note 1.
- Release note 2.

### Deprecated
- Deprecated feature 1
- Future removal 2

### Fixed
- Bug fix 1
- sub bug 1
- sub bug 2
- Bug fix 2

### Removed
- Deprecated feature 2
- Future removal 1

### Security
- Known issue 1
- Known issue 2

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
"""


changelog_as_dict = {
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
        "removed": ["Deprecated feature 2", "Future removal 1"],
        "security": ["Known issue 1", "Known issue 2"],
        "metadata": {
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
    },
    "1.1.0": {
        "changed": [
            "Enhancement 1 (1.1.0)",
            "sub enhancement 1",
            "sub enhancement 2",
            "Enhancement 2 (1.1.0)",
        ],
        "metadata": {
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
    },
    "1.0.1": {
        "fixed": [
            "Bug fix 1 (1.0.1)",
            "sub bug 1",
            "sub bug 2",
            "Bug fix 2 (1.0.1)",
        ],
        "metadata": {
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
    },
    "1.0.0": {
        "deprecated": ["Known issue 1 (1.0.0)", "Known issue 2 (1.0.0)"],
        "metadata": {
            "release_date": "2017-04-10",
            "version": "1.0.0",
            "semantic_version": {
                "buildmetadata": None,
                "major": 1,
                "minor": 0,
                "patch": 0,
                "prerelease": None,
            },
        },
    },
}


def test_changelog_dont_have_2_newline_at_eof():
    assert keepachangelog.from_dict(changelog_as_dict) == changelog_as_text
