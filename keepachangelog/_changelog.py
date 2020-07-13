import re
from typing import Dict, List

# Release pattern should match lines like: "## [0.0.1] - 2020-12-31" or ## [Unreleased]
release_pattern = re.compile(r"^## \[(.*)\](?: - (.*))?$")


def is_release(line: str, show_unreleased: bool) -> bool:
    match = release_pattern.fullmatch(line)
    if match and (not show_unreleased and match.group(1) == "Unreleased"):
        return False
    return match is not None


def add_release(changes: Dict[str, dict], line: str) -> dict:
    release_info = release_pattern.fullmatch(line)
    return changes.setdefault(
        release_info.group(1),
        {"version": release_info.group(1), "release_date": release_info.group(2)},
    )


categories = {
    "### Added": "added",
    "### Changed": "changed",
    "### Deprecated": "deprecated",
    "### Removed": "removed",
    "### Fixed": "fixed",
    "### Security": "security",
}


def is_category(line: str) -> bool:
    return line in categories


def add_category(release: dict, line: str) -> List[str]:
    return release.setdefault(categories[line], [])


# Link pattern should match lines like: "[1.2.3]: https://github.com/user/project/releases/tag/v0.0.1"
link_pattern = re.compile(r"^\[(.*)\]: (.*)$")


def is_information(line: str) -> bool:
    return line and not link_pattern.fullmatch(line)


def add_information(category: List[str], line: str):
    category.append(line.lstrip(" *-").rstrip(" -"))


def to_dict(changelog_path: str, *, show_unreleased: bool = False) -> Dict[str, dict]:
    changes = {}
    with open(changelog_path) as change_log:
        release = {}
        category = []
        for line in change_log:
            line = line.strip(" \n")

            if is_release(line, show_unreleased):
                release = add_release(changes, line)
            elif is_category(line):
                category = add_category(release, line)
            elif is_information(line):
                add_information(category, line)

    return changes
