import os
import os.path

import pytest

import keepachangelog


content = """# Header Title
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

## [Unreleased]
### Added
- Enhancement 1
- sub enhancement 1

## [1.2.0] - 2018-06-01
### Added
- Cool feature

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


@pytest.fixture
def changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(content)
    return changelog_file_path


def test_changelog_with_different_header_to_dict(changelog):
    assert keepachangelog.to_dict(changelog)["header"] == {
        "title": "Header Title",
        "text": [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor",
            "in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "",
        ],
    }


def test_changelog_with_different_header_from_dict(changelog):
    assert (
        keepachangelog.from_dict(
            keepachangelog.to_dict(changelog, show_unreleased=True)
        )
        == content
    )
