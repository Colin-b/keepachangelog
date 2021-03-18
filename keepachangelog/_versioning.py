import re
from typing import Tuple, Optional


def contains_breaking_changes(unreleased: dict) -> bool:
    return "removed" in unreleased or "changed" in unreleased


def only_contains_bug_fixes(unreleased: dict) -> bool:
    # unreleased contains at least 2 entries: version and release_date
    return "fixed" in unreleased and len(unreleased) == 3


def bump_major(version: str) -> str:
    major, *_ = to_semantic(version)
    return from_semantic(major + 1, 0, 0)


def bump_minor(version: str) -> str:
    major, minor, _ = to_semantic(version)
    return from_semantic(major, minor + 1, 0)


def bump_patch(version: str) -> str:
    major, minor, patch = to_semantic(version)
    return from_semantic(major, minor, patch + 1)


def bump(unreleased: dict, version: str) -> str:
    if contains_breaking_changes(unreleased):
        return bump_major(version)
    if only_contains_bug_fixes(unreleased):
        return bump_patch(version)
    return bump_minor(version)


def actual_version(changelog: dict) -> Optional[str]:
    versions = sorted(changelog.keys())
    current_version = versions.pop() if versions else None
    while "Unreleased" == current_version:
        current_version = versions.pop() if versions else None
    return current_version


def guess_unreleased_version(changelog: dict) -> Tuple[Optional[str], str]:
    unreleased = changelog.get("Unreleased", {})
    if not unreleased:
        raise Exception(
            "Unable to guess unreleased version because there is not Unreleased section within changelog."
        )

    version = actual_version(changelog)
    return version, bump(unreleased, version)


def to_semantic(version: Optional[str]) -> Tuple[int, int, int]:
    if not version:
        return 0, 0, 0

    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))

    raise Exception(f"{version} is not following semantic versioning.")


def from_semantic(major: int, minor: int, patch: int) -> str:
    return f"{major}.{minor}.{patch}"
