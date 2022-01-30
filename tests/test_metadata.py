from datetime import date

import pytest

from keepachangelog._changelog_dataclasses import Metadata


class TestMetadata:
    @pytest.mark.parametrize(
        ["line", "version", "raw_release_date", "release_date"],
        [
            pytest.param(
                "## [1.2.3] - 2018-05-01", "1.2.3", "2018-05-01", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - 01-05-2018", "1.2.3", "01-05-2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - 2018/05/01", "1.2.3", "2018/05/01", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - 01/05/2018", "1.2.3", "01/05/2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - May 01, 2018", "1.2.3", "May 01, 2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - May 01, 2018", "1.2.3", "May 01, 2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - May 01 2018", "1.2.3", "May 01 2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - May 01 2018", "1.2.3", "May 01 2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] - 1er mai 2018", "1.2.3", "1er mai 2018", "1er mai 2018"
            ),
            pytest.param(
                "## 1.2.3 May 01 2018", "1.2.3", "May 01 2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## 1.2.3 (May 01 2018)", "1.2.3", "May 01 2018", date(2018, 5, 1)
            ),
            pytest.param(
                "## [1.2.3] (May 01 2018)", "1.2.3", "May 01 2018", date(2018, 5, 1)
            ),
            pytest.param("## [master]", "master", None, None),
            pytest.param("## Develop", "Develop", None, None),
        ],
    )
    def test_parse_release_line(self, line, version, raw_release_date, release_date):
        metadata = Metadata.from_release_line(line)
        assert metadata.version == version
        assert metadata.release_date == release_date
        assert metadata.raw_release_date == raw_release_date
