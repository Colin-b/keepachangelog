import pytest

import keepachangelog


def test_changelog_not_found():
    with pytest.raises(FileNotFoundError):
        keepachangelog.to_dict("do not exists")
