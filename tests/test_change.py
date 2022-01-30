from datetime import date

import pytest

from keepachangelog._changelog_dataclasses import Change, Category
from keepachangelog._versioning import UnmatchingSemanticVersion


class TestChange:
    def test_construction_with_metadata_as_dict(self):
        change = Change(metadata={"version": "1.0.0", "release_date": "2018-5-1"})
        assert change.metadata.version == "1.0.0"
        assert str(change.metadata.semantic_version) == "1.0.0"
        assert change.metadata.release_date == date(2018, 5, 1)
        assert change.metadata.raw_release_date == "2018-5-1"

    def test_construction_with_metadata_as_dict_bad_semver(self):
        with pytest.raises(UnmatchingSemanticVersion):
            change = Change(
                metadata={
                    "version": "1.0.0",
                    "semantic_version": {
                        "major": 1,
                        "minor": 2,
                        "patch": 3,
                        "prerelease": None,
                        "buildmetadata": None,
                    },
                }
            )

    def test_construction_with_metadata_as_dict_bad_semver_diff_bmd(self):
        with pytest.raises(UnmatchingSemanticVersion):
            change = Change(
                metadata={
                    "version": "1.0.0+linux",
                    "semantic_version": {
                        "major": 1,
                        "minor": 0,
                        "patch": 0,
                        "prerelease": None,
                        "buildmetadata": "win64",
                    },
                }
            )

    def test_construction_with_metadata_as_dict_only_semver(self):
        change = Change(
            metadata={
                "semantic_version": {
                    "major": 1,
                    "minor": 0,
                    "patch": 0,
                    "prerelease": None,
                    "buildmetadata": "win64",
                },
            }
        )
        assert change.metadata.version == "1.0.0+win64"

    def test_construction_with_category(self):
        change = Change(
            uncategorized=["line1", "line2"],
            changed=["line3", "line4"],
        )
        assert isinstance(change.uncategorized, Category)
        assert list(change.uncategorized) == ["line1", "line2"]
        assert isinstance(change.changed, Category)
        assert list(change.changed) == ["line3", "line4"]
