import datetime
import os
import os.path

import pytest
from freezegun import freeze_time

import keepachangelog
import keepachangelog._changelog

_date_time_for_tests = datetime.datetime(2021, 3, 19, 15, 5, 5, 663979)


@pytest.fixture
def major_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "MAJOR_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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

## [1.1.0.dev0] - 2018-05-31
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

[Unreleased]: https://github.test_url/test_project/compare/v1.1.0...HEAD
[1.1.0]: https://github.test_url/test_project/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
"""
        )
    return changelog_file_path


@pytest.fixture
def minor_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "MINOR_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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

## [1.0.1.dev0] - 2018-05-31
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


@pytest.fixture
def patch_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "PATCH_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Bug fix 1
 - sub bug 1
 * sub bug 2
- Bug fix 2

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

[Unreleased]: https://github.test_url/test_project/compare/v1.1.0...HEAD
[1.1.0]: https://github.test_url/test_project/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
"""
        )
    return changelog_file_path


@pytest.fixture
def first_major_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "FIRST_MAJOR_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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

[Unreleased]: https://github.test_url/test_project
"""
        )
    return changelog_file_path


@pytest.fixture
def first_minor_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "FIRST_MINOR_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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

[Unreleased]: https://github.test_url/test_project
"""
        )
    return changelog_file_path


@pytest.fixture
def first_patch_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "FIRST_PATCH_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Bug fix 1
 - sub bug 1
 * sub bug 2
- Bug fix 2

[Unreleased]: https://github.test_url/test_project
"""
        )
    return changelog_file_path


@pytest.fixture
def empty_unreleased_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "EMPTY_UNRELEASED_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

[Unreleased]: https://github.test_url/test_project
"""
        )
    return changelog_file_path


@pytest.fixture
def empty_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "EMPTY_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""
        )
    return changelog_file_path


@pytest.fixture
def non_semantic_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "NON_SEMANTIC_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Enhancement 1 (1.1.0)

## [20180531] - 2018-05-31
### Changed
- Enhancement 1 (1.1.0)
- sub *enhancement 1*
- sub enhancement 2
- Enhancement 2 (1.1.0)

[Unreleased]: https://github.test_url/test_project/compare/v20180531...HEAD
[20180531]: https://github.test_url/test_project/releases/tag/v20180531
"""
        )
    return changelog_file_path


@pytest.fixture
def unstable_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "UNSTABLE_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Enhancement 1 (1.1.0)

## [2.5.0b51] - 2018-05-31
### Changed
- Enhancement 1 (1.1.0)
- sub *enhancement 1*
- sub enhancement 2
- Enhancement 2 (1.1.0)
"""
        )
    return changelog_file_path


@pytest.fixture
def major_digit_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "MAJOR_DIGIT_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Enhancement

## [10.9.90] - 2018-05-31
### Changed
- Enhancement

## [9.10.100] - 2018-05-31
### Changed
- Enhancement
"""
        )
    return changelog_file_path


@pytest.fixture
def minor_digit_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "MINOR_DIGIT_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Enhancement

## [9.10.90] - 2018-05-31
### Added
- Enhancement

## [9.9.100] - 2018-05-31
### Added
- Enhancement
"""
        )
    return changelog_file_path


@pytest.fixture
def patch_digit_changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "PATCH_DIGIT_CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Enhancement

## [9.9.10] - 2018-05-31
### Fixed
- Enhancement

## [9.9.9] - 2018-05-31
### Fixed
- Enhancement
"""
        )
    return changelog_file_path

@freeze_time(_date_time_for_tests)
def test_major_release(major_changelog):
    assert keepachangelog.release(major_changelog) == "2.0.0"
    with open(major_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2021-03-19
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

## [1.1.0.dev0] - 2018-05-31
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

[Unreleased]: https://github.test_url/test_project/compare/v2.0.0...HEAD
[2.0.0]: https://github.test_url/test_project/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.test_url/test_project/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
"""
        )


@freeze_time(_date_time_for_tests)
def test_minor_release(minor_changelog):
    assert keepachangelog.release(minor_changelog) == "1.2.0"
    with open(minor_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2021-03-19
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

## [1.0.1.dev0] - 2018-05-31
### Fixed
- Bug fix 1 (1.0.1)
- sub bug 1
- sub bug 2
- Bug fix 2 (1.0.1)

## [1.0.0] - 2017-04-10
### Deprecated
- Known issue 1 (1.0.0)
- Known issue 2 (1.0.0)

[Unreleased]: https://github.test_url/test_project/compare/v1.2.0...HEAD
[1.2.0]: https://github.test_url/test_project/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.test_url/test_project/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
"""
        )


@freeze_time(_date_time_for_tests)
def test_major_digit_release(major_digit_changelog):
    assert keepachangelog.release(major_digit_changelog) == "11.0.0"
    with open(major_digit_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [11.0.0] - 2021-03-19
### Changed
- Enhancement

## [10.9.90] - 2018-05-31
### Changed
- Enhancement

## [9.10.100] - 2018-05-31
### Changed
- Enhancement
"""
        )


@freeze_time(_date_time_for_tests)
def test_minor_digit_release(minor_digit_changelog):
    assert keepachangelog.release(minor_digit_changelog) == "9.11.0"
    with open(minor_digit_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [9.11.0] - 2021-03-19
### Added
- Enhancement

## [9.10.90] - 2018-05-31
### Added
- Enhancement

## [9.9.100] - 2018-05-31
### Added
- Enhancement
"""
        )


@freeze_time(_date_time_for_tests)
def test_patch_digit_release(patch_digit_changelog):
    assert keepachangelog.release(patch_digit_changelog) == "9.9.11"
    with open(patch_digit_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [9.9.11] - 2021-03-19
### Fixed
- Enhancement

## [9.9.10] - 2018-05-31
### Fixed
- Enhancement

## [9.9.9] - 2018-05-31
### Fixed
- Enhancement
"""
        )


@freeze_time(_date_time_for_tests)
def test_sorted_major_digit_semantic_release(major_digit_changelog):
    assert keepachangelog.to_sorted_semantic(
        keepachangelog.to_raw_dict(major_digit_changelog)
    ) == [
        (
            "9.10.100",
            {
                "buildmetadata": None,
                "major": 9,
                "minor": 10,
                "patch": 100,
                "prerelease": None,
            },
        ),
        (
            "10.9.90",
            {
                "buildmetadata": None,
                "major": 10,
                "minor": 9,
                "patch": 90,
                "prerelease": None,
            },
        ),
    ]


@freeze_time(_date_time_for_tests)
def test_sorted_minor_digit_semantic_release(minor_digit_changelog):
    assert keepachangelog.to_sorted_semantic(
        keepachangelog.to_raw_dict(minor_digit_changelog)
    ) == [
        (
            "9.9.100",
            {
                "buildmetadata": None,
                "major": 9,
                "minor": 9,
                "patch": 100,
                "prerelease": None,
            },
        ),
        (
            "9.10.90",
            {
                "buildmetadata": None,
                "major": 9,
                "minor": 10,
                "patch": 90,
                "prerelease": None,
            },
        ),
    ]


@freeze_time(_date_time_for_tests)
def test_sorted_patch_digit_semantic_release(patch_digit_changelog):
    assert keepachangelog.to_sorted_semantic(
        keepachangelog.to_raw_dict(patch_digit_changelog)
    ) == [
        (
            "9.9.9",
            {
                "buildmetadata": None,
                "major": 9,
                "minor": 9,
                "patch": 9,
                "prerelease": None,
            },
        ),
        (
            "9.9.10",
            {
                "buildmetadata": None,
                "major": 9,
                "minor": 9,
                "patch": 10,
                "prerelease": None,
            },
        ),
    ]


@freeze_time(_date_time_for_tests)
def test_patch_release(patch_changelog):
    assert keepachangelog.release(patch_changelog) == "1.1.1"
    with open(patch_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.1] - 2021-03-19
### Fixed
- Bug fix 1
 - sub bug 1
 * sub bug 2
- Bug fix 2

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

[Unreleased]: https://github.test_url/test_project/compare/v1.1.1...HEAD
[1.1.1]: https://github.test_url/test_project/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.test_url/test_project/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.test_url/test_project/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.test_url/test_project/releases/tag/v1.0.0
"""
        )


@freeze_time(_date_time_for_tests)
def test_first_major_release(first_major_changelog):
    assert keepachangelog.release(first_major_changelog) == "1.0.0"
    with open(first_major_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2021-03-19
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

[Unreleased]: https://github.test_url/test_project
[1.0.0]: https://github.test_url/test_project
"""
        )


@freeze_time(_date_time_for_tests)
def test_first_minor_release(first_minor_changelog):
    assert keepachangelog.release(first_minor_changelog) == "0.1.0"
    with open(first_minor_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2021-03-19
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

[Unreleased]: https://github.test_url/test_project
[0.1.0]: https://github.test_url/test_project
"""
        )


@freeze_time(_date_time_for_tests)
def test_first_patch_release(first_patch_changelog):
    assert keepachangelog.release(first_patch_changelog) == "0.0.1"
    with open(first_patch_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2021-03-19
### Fixed
- Bug fix 1
 - sub bug 1
 * sub bug 2
- Bug fix 2

[Unreleased]: https://github.test_url/test_project
[0.0.1]: https://github.test_url/test_project
"""
        )


def test_empty_release(empty_changelog):
    assert not keepachangelog.release(empty_changelog)


def test_empty_unreleased_release(empty_unreleased_changelog):
    assert not keepachangelog.release(empty_unreleased_changelog)


def test_non_semantic_release(non_semantic_changelog):
    with pytest.raises(Exception) as exception_info:
        keepachangelog.release(non_semantic_changelog)
    assert (
        str(exception_info.value)
        == "20180531 is not following semantic versioning. Check https://semver.org for more information."
    )


@freeze_time(_date_time_for_tests)
def test_first_stable_release(unstable_changelog):
    assert keepachangelog.release(unstable_changelog) == "2.5.0"
    with open(unstable_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.5.0] - 2021-03-19
### Changed
- Enhancement 1 (1.1.0)

## [2.5.0b51] - 2018-05-31
### Changed
- Enhancement 1 (1.1.0)
- sub *enhancement 1*
- sub enhancement 2
- Enhancement 2 (1.1.0)
"""
        )


@freeze_time(_date_time_for_tests)
def test_custom_release(unstable_changelog):
    assert (
        keepachangelog.release(unstable_changelog, new_version="2.5.0b52") == "2.5.0b52"
    )
    with open(unstable_changelog) as file:
        assert (
            file.read()
            == """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.5.0b52] - 2021-03-19
### Changed
- Enhancement 1 (1.1.0)

## [2.5.0b51] - 2018-05-31
### Changed
- Enhancement 1 (1.1.0)
- sub *enhancement 1*
- sub enhancement 2
- Enhancement 2 (1.1.0)
"""
        )
