import textwrap

import pytest

from keepachangelog._changelog_dataclasses import Changelog, SemanticVersion


class TestChangelog:
    def test_several_unreleased(self):
        md = textwrap.dedent(
            """
            ## master
            - line 1
            ## develop
            ### changed
            - line 2
            ## [1.0.0] 2018-5-1
            - line 3
            """
        )
        changelog = Changelog()
        changelog.streamlines(md.splitlines())
        assert len(changelog.unreleased) == 2
        assert len(changelog.changes) == 3
        with pytest.raises(AttributeError):
            un = changelog.unreleased_unique

    def test_released_no_version(self):
        md = textwrap.dedent(
            """
            ## [] 2018-5-1
            - line 1
            """
        )
        changelog = Changelog()
        changelog.streamlines(md.splitlines())
        assert len(changelog.unreleased) == 0
        assert len(changelog.changes) == 1
        change = list(changelog.changes.values())[0]
        assert change.is_released
        assert not change.is_empty
        assert (
            change.metadata.semantic_version
            == change.metadata.semantic_version_strict
            == SemanticVersion.initial_version()
        )
        assert changelog.current_version == SemanticVersion.initial_version()
