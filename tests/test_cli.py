import os

import pytest

from keepachangelog.__main__ import main as cli
from keepachangelog.version import __version__


@pytest.fixture
def changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "CHANGELOG.md")
    with open(changelog_file_path, mode="wt", encoding="utf-8") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Breaking change

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
- Known issue 1 (1.0.0) 漢字
- Known issue 2 (1.0.0)
"""
        )
    return changelog_file_path


@pytest.fixture
def changelog_without_unreleased(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "CHANGELOG_without_unreleased.md")
    with open(changelog_file_path, mode="wt", encoding="utf-8") as file:
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2017-04-10
### Deprecated
- Known issue 1 (1.0.0) 漢字
- Known issue 2 (1.0.0)
"""
        )
    return changelog_file_path


def test_print_help(changelog: str, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit) as exc:
        cli(["--help"])

    assert exc.value.args[0] == 0

    captured = capsys.readouterr()

    assert captured.err == ""
    assert "usage: keepachangelog [-h] [-v] {show,release} ..." in captured.out


def test_print_version(changelog: str, capsys: pytest.CaptureFixture):
    with pytest.raises(SystemExit) as exc:
        cli(["--version"])

    assert exc.value.args[0] == 0

    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.strip() == f"keepachangelog {__version__}"


def test_show_release_raw(changelog: str, capsys: pytest.CaptureFixture):
    cli(["show", "1.0.0", changelog])

    captured = capsys.readouterr()

    assert captured.err == ""
    assert (
        captured.out.strip()
        == """### Deprecated
- Known issue 1 (1.0.0) 漢字
- Known issue 2 (1.0.0)"""
    )


def test_create_release_automatic_version(
    changelog: str, capsys: pytest.CaptureFixture
):
    cli(["release", "-f", changelog])

    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.strip() == "2.0.0"


def test_create_release_nothing_to_release(
    changelog_without_unreleased: str, capsys: pytest.CaptureFixture
):
    with pytest.raises(SystemExit) as cm:
        cli(["release", "-f", changelog_without_unreleased])
    assert cm.value.code == 2

    captured = capsys.readouterr()

    assert captured.err == f"{changelog_without_unreleased} must contains a description of the release content (within Unreleased section)."
    assert captured.out == ""


def test_create_release_specific_version(changelog: str, capsys: pytest.CaptureFixture):
    cli(["release", "3.2.1", "-f", changelog])

    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.strip() == "3.2.1"
