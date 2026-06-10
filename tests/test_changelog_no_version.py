import os
import os.path

import pytest

import keepachangelog

from tests.conftest import to_dict_ignore_header


@pytest.fixture
def changelog(tmpdir):
    changelog_file_path = os.path.join(tmpdir, "CHANGELOG.md")
    with open(changelog_file_path, "wt") as file:
        file.write("This is the changelog content.\n")
        file.write("This is the second line.\n")
    return changelog_file_path


def test_changelog_without_versions(changelog):
    assert to_dict_ignore_header(changelog) == {}


def test_raw_changelog_without_versions(changelog):
    assert keepachangelog.to_raw_dict(changelog) == {}
