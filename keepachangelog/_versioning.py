import re
from typing import Tuple, Optional


initial_semantic_version = {
    "major": 0,
    "minor": 0,
    "patch": 0,
    "prerelease": None,
    "buildmetadata": None,
}


class InvalidSemanticVersion(Exception):
    def __init__(self, version: str):
        super().__init__(
            f"{version} is not following semantic versioning. Check https://semver.org for more information."
        )


def contains_breaking_changes(unreleased: dict) -> bool:
    return "removed" in unreleased or "changed" in unreleased


def only_contains_bug_fixes(unreleased: dict) -> bool:
    return ["fixed"] == list(unreleased)


def bump_major(semantic_version: dict):
    semantic_version["major"] += 1
    semantic_version["minor"] = 0
    semantic_version["patch"] = 0
    semantic_version["prerelease"] = None
    semantic_version["buildmetadata"] = None


def bump_minor(semantic_version: dict) -> str:
    semantic_version["minor"] += 1
    semantic_version["patch"] = 0
    semantic_version["prerelease"] = None
    semantic_version["buildmetadata"] = None


def bump_patch(semantic_version: dict) -> str:
    semantic_version["patch"] += 1
    semantic_version["prerelease"] = None
    semantic_version["buildmetadata"] = None


def bump(unreleased: dict, semantic_version: dict) -> dict:
    if semantic_version["prerelease"]:
        semantic_version["prerelease"] = None
        semantic_version["buildmetadata"] = None
    elif contains_breaking_changes(unreleased):
        bump_major(semantic_version)
    elif only_contains_bug_fixes(unreleased):
        bump_patch(semantic_version)
    else:
        bump_minor(semantic_version)
    return semantic_version


def semantic_order(version: Tuple[str, dict]) -> str:
    _, semantic_version = version
    # Ensure release is "bigger than" pre-release
    pre_release_order = (
        f"0{semantic_version['prerelease']}" if semantic_version["prerelease"] else "1"
    )
    return f"{semantic_version['major']}.{semantic_version['minor']}.{semantic_version['patch']}.{pre_release_order}"


def actual_version(changelog: dict) -> Tuple[Optional[str], dict]:
    versions = sorted(
        [
            (version, to_semantic(version))
            for version in changelog.keys()
            if version != "unreleased"
        ],
        key=semantic_order,
    )
    return versions.pop() if versions else (None, initial_semantic_version.copy())


def guess_unreleased_version(
    changelog: dict, current_semantic_version: dict
) -> Optional[str]:
    unreleased = changelog.get("unreleased", {})
    # Only keep user provided entries
    unreleased = unreleased.copy()
    unreleased.pop("metadata", None)
    if unreleased:
        return from_semantic(bump(unreleased, current_semantic_version))


semantic_versioning = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:[-\.]?(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def to_semantic(version: Optional[str]) -> dict:
    if not version:
        return initial_semantic_version.copy()

    match = semantic_versioning.fullmatch(version)
    if match:
        return {
            key: int(value) if key in ("major", "minor", "patch") else value
            for key, value in match.groupdict().items()
        }

    raise InvalidSemanticVersion(version)


def from_semantic(semantic_version: dict) -> str:
    return f"{semantic_version['major']}.{semantic_version['minor']}.{semantic_version['patch']}"
