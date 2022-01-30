import pytest
from keepachangelog._changelog_dataclasses import SemanticVersion
from keepachangelog._versioning import InvalidSemanticVersion


@pytest.fixture
def initial_semantic_version() -> SemanticVersion:
    return SemanticVersion.initial_version()


@pytest.fixture
def initial_semantic_dict(initial_semantic_version: SemanticVersion) -> dict:
    return initial_semantic_version.to_dict(force=True)


class TestToSemantic:
    def test_empty_str(self, initial_semantic_dict):
        assert SemanticVersion.to_semantic("") == initial_semantic_dict

    def test_default(self, initial_semantic_dict):
        assert SemanticVersion.to_semantic() == initial_semantic_dict

    def test_none(self, initial_semantic_dict):
        assert SemanticVersion.to_semantic(None) == initial_semantic_dict


class TestFromVersionString:
    @pytest.mark.parametrize(
        ["version_string", "expected_tuple"],
        [
            pytest.param("1.2.3", (1, 2, 3, None, None), id="Ma.Mi.Pa"),
            pytest.param("1.2.3b1", (1, 2, 3, "b1", None), id="Ma.Mi.PaPr"),
            pytest.param("1.2.3-b1", (1, 2, 3, "b1", None), id="Ma.Mi.Pa-Pr"),
            pytest.param("1.2.3.b1", (1, 2, 3, "b1", None), id="Ma.Mi.Pa.Pr"),
            pytest.param("1.2.3+42", (1, 2, 3, None, "42"), id="Ma.Mi.Pa+BMD"),
            pytest.param("1.2.3b1+42", (1, 2, 3, "b1", "42"), id="Ma.Mi.PaPr+BMD"),
            pytest.param("1.2.3-b1+42", (1, 2, 3, "b1", "42"), id="Ma.Mi.Pa-Pr+BMD"),
            pytest.param(
                "1.2.3.b1.42", (1, 2, 3, "b1.42", None), id="Ma.Mi.Pa.Pr1.Pr2"
            ),
            pytest.param(
                "1.2.3.4.8.15+16.23.42",
                (1, 2, 3, "4.8.15", "16.23.42"),
                id="Ma.Mi.Pa.Pr1.Pr2.Pr3+BMD1.BMD2.BMD3",
            ),
        ],
    )
    def test_valid(self, version_string, expected_tuple):
        assert (
            SemanticVersion.from_version_string(version_string).to_tuple()
            == expected_tuple
        )

    @pytest.mark.parametrize(
        ["version_string"],
        [
            pytest.param("1", id="Ma"),
            pytest.param("1.2", id="Ma.Mi"),
            pytest.param("a.2.2", id="MaS.Mi.Pa"),
            pytest.param("1.b.3", id="Ma.MiS.Pa"),
            pytest.param("1.2.c", id="Ma.Mi.PaS"),
            pytest.param("1.2-alpha", id="Ma.Mi-Pr"),
            pytest.param("1.2-alpha+dev", id="Ma.Mi-Pr+BMD"),
            pytest.param("1.2+dev", id="Ma.Mi+BMD"),
        ],
    )
    def test_invalid(self, version_string):
        with pytest.raises(InvalidSemanticVersion):
            SemanticVersion.from_version_string(version_string).to_tuple()

    @pytest.mark.parametrize(
        ["ver_low", "ver_high"],
        [
            pytest.param("1.0.0", "1.0.1", id="patch"),
            pytest.param("1.0.0", "1.1.0", id="minor"),
            pytest.param("1.0.0", "2.0.0", id="major"),
            pytest.param("1.0.0-dev", "1.0.0", id="prerelease-release"),
            pytest.param("1.0.0-dev1", "1.0.0-dev2", id="prerelease-prerelease"),
            pytest.param("1.0.0-dev1+2", "1.0.0-dev2+1", id="pre1.BMD-pre2.BMD"),
        ],
    )
    def test_ordering_less(self, ver_low, ver_high):
        semver_low = SemanticVersion.from_version_string(ver_low)
        semver_high = SemanticVersion.from_version_string(ver_high)
        assert semver_low < semver_high

    @pytest.mark.parametrize(
        ["version1", "version2"],
        [
            pytest.param("1.0.0", "1.0.0", id="same"),
            pytest.param("1.0.0+1", "1.0.0+2", id="BMD-BMD"),
            pytest.param("1.0.0+posix", "1.0.0+win64", id="BMD_os-BMD_os"),
        ],
    )
    def test_ordering_equal(self, version1, version2):
        semver1 = SemanticVersion.from_version_string(version1)
        semver2 = SemanticVersion.from_version_string(version2)
        assert semver1 == semver2

    def test_to_dict(self):
        assert SemanticVersion(0, 0, 0).to_dict() is None

    def test_to_dict_force(self):
        assert SemanticVersion(0, 0, 0).to_dict(force=True) == {
            "major": 0,
            "minor": 0,
            "patch": 0,
            "prerelease": None,
            "buildmetadata": None,
        }
