import datetime
import re
from typing import Dict, List, Optional, Iterable, Union

from keepachangelog._versioning import (
    actual_version,
    guess_unreleased_version,
    to_semantic,
    InvalidSemanticVersion,
)


def is_release(line: str) -> bool:
    return line.startswith("## ")


def add_release(changes: Dict[str, dict], line: str) -> dict:
    release_line = line[3:].lower().strip(" ")
    # A release is separated by a space between version and release date
    # Release pattern should match lines like: "[0.0.1] - 2020-12-31" or [Unreleased]
    version, release_date = (
        release_line.split(" ", maxsplit=1)
        if " " in release_line
        else (release_line, None)
    )
    version = unlink(version)

    metadata = {"version": version, "release_date": extract_date(release_date)}
    try:
        metadata["semantic_version"] = to_semantic(version)
    except InvalidSemanticVersion:
        pass

    return changes.setdefault(version, {"metadata": metadata})


def unlink(value: str) -> str:
    return value.lstrip("[").rstrip("]")


def extract_date(date: str) -> str:
    if not date:
        return date

    return date.lstrip(" -(").rstrip(" )")


def is_category(line: str) -> bool:
    return line.startswith("### ")


def add_category(release: dict, line: str) -> List[str]:
    category = line[4:].lower().strip(" ")
    return release.setdefault(category, [])


# Link pattern should match lines like: "[1.2.3]: https://github.com/user/project/releases/tag/v0.0.1"
link_pattern = re.compile(r"^\[(.*)\]: (.*)$")


def is_link(line: str) -> bool:
    return link_pattern.fullmatch(line) is not None


def add_information(category: List[str], line: str):
    category.append(line.lstrip(" *-").rstrip(" -"))


def to_dict(
    changelog_path: Union[str, Iterable[str]], *, show_unreleased: bool = False
) -> Dict[str, dict]:
    """
    Convert changelog markdown file following keep a changelog format into python dict.

    :param changelog_path: Path to the changelog file, or context manager providing iteration on lines.
    :param show_unreleased: Add unreleased section (if any) to the resulting dictionary.
    :return python dict containing version as key and related changes as value.
    """
    # Allow for changelog as a file path or as a context manager providing content
    try:
        with open(changelog_path, encoding="utf-8") as change_log:
            return _to_dict(change_log, show_unreleased)
    except TypeError:
        return _to_dict(changelog_path, show_unreleased)


def _to_dict(change_log: Iterable[str], show_unreleased: bool) -> Dict[str, dict]:
    changes = {}
    # As URLs can be defined before actual usage, maintain a separate dict
    urls = {}
    current_release = {}
    category = []
    for line in change_log:
        line = line.strip(" \n")

        if is_release(line):
            current_release = add_release(changes, line)
            category = current_release.setdefault("uncategorized", [])
        elif is_category(line):
            category = add_category(current_release, line)
        elif is_link(line):
            link_match = link_pattern.fullmatch(line)
            urls[link_match.group(1).lower()] = link_match.group(2)
        elif line:
            add_information(category, line)

    # Add url for each version (create version if not existing)
    for version, url in urls.items():
        changes.setdefault(version, {"metadata": {"version": version}})["metadata"][
            "url"
        ] = url

    # Avoid empty uncategorized
    unreleased_version = None
    for version, current_release in changes.items():
        metadata = current_release["metadata"]
        if not current_release.get("uncategorized"):
            current_release.pop("uncategorized", None)

        # If there is an empty release date, it identify the unreleased section
        if ("release_date" in metadata) and not metadata["release_date"]:
            unreleased_version = version

    if not show_unreleased:
        changes.pop(unreleased_version, None)

    return changes


def from_dict(changes: Dict[str, dict]):
    content = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n"""

    for current_release in changes.values():
        metadata = current_release["metadata"]
        content += f"\n## [{metadata['version'].capitalize()}]"

        if metadata.get("release_date"):
            content += f" - {metadata['release_date']}"

        uncategorized = current_release.get("uncategorized", [])
        for category_content in uncategorized:
            content += f"\n* {category_content}"
        if uncategorized:
            content += "\n"

        for category_name, category_content in current_release.items():
            if category_name in ["metadata", "uncategorized"]:
                continue

            content += f"\n### {category_name.capitalize()}"

            for categorized in category_content:
                content += f"\n- {categorized}"

            content += "\n"

    urls_content = []
    for current_release in changes.values():
        metadata = current_release["metadata"]
        if not metadata.get("url"):
            continue
        urls_content.append(f"[{metadata['version'].capitalize()}]: {metadata['url']}")

    if urls_content:
        content += "\n"
        content += "\n".join(urls_content)
        content += "\n"

    return content


def to_raw_dict(changelog_path: str) -> Dict[str, dict]:
    changes = {}
    # As URLs can be defined before actual usage, maintain a separate dict
    urls = {}
    with open(changelog_path, encoding="utf-8") as change_log:
        current_release = {}
        for line in change_log:
            clean_line = line.strip(" \n")

            if is_release(clean_line):
                current_release = add_release(changes, clean_line)
            elif is_link(clean_line):
                link_match = link_pattern.fullmatch(clean_line)
                urls[link_match.group(1).lower()] = link_match.group(2)
            elif clean_line:
                current_release["raw"] = current_release.get("raw", "") + line

    # Add url for each version (create version if not existing)
    for version, url in urls.items():
        changes.setdefault(version, {"metadata": {"version": version}})["metadata"][
            "url"
        ] = url

    unreleased_version = None
    for version, current_release in changes.items():
        metadata = current_release["metadata"]
        # If there is an empty release date, it identify the unreleased section
        if ("release_date" in metadata) and not metadata["release_date"]:
            unreleased_version = version

    changes.pop(unreleased_version, None)

    return changes


def release(changelog_path: str, new_version: str = None) -> Optional[str]:
    """
    Release a new version based on changelog unreleased content.

    :param changelog_path: Path to the changelog file.
    :param new_version: The new version to use instead of trying to guess one.
    :return: The new version, None if there was no change to release.
    """
    changelog = to_dict(changelog_path, show_unreleased=True)
    current_version, current_semantic_version = actual_version(changelog)
    if not new_version:
        new_version = guess_unreleased_version(changelog, current_semantic_version)
    if new_version:
        release_version(changelog_path, current_version, new_version)
    return new_version


def release_version(
    changelog_path: str, current_version: Optional[str], new_version: str
):
    unreleased_link_pattern = re.compile(r"^\[Unreleased\]: (.*)$", re.DOTALL)
    lines = []
    with open(changelog_path, encoding="utf-8") as change_log:
        for line in change_log.readlines():
            # Move Unreleased section to new version
            if re.fullmatch(r"^## \[Unreleased\].*$", line, re.DOTALL):
                lines.append(line)
                lines.append("\n")
                lines.append(
                    f"## [{new_version}] - {datetime.date.today().isoformat()}\n"
                )
            # Add new version link and update Unreleased link
            elif unreleased_link_pattern.fullmatch(line):
                unreleased_compare_pattern = re.fullmatch(
                    r"^.*/(.*)\.\.\.(\w*).*$", line, re.DOTALL
                )
                # Unreleased link compare previous version to HEAD (unreleased tag)
                if unreleased_compare_pattern:
                    new_unreleased_link = line.replace(current_version, new_version)
                    lines.append(new_unreleased_link)
                    current_tag = unreleased_compare_pattern.group(1)
                    unreleased_tag = unreleased_compare_pattern.group(2)
                    new_tag = current_tag.replace(current_version, new_version)
                    lines.append(
                        line.replace(new_version, current_version)
                        .replace(unreleased_tag, new_tag)
                        .replace("Unreleased", new_version)
                    )
                # Consider that there is no way to know how to create a link to compare versions
                else:
                    lines.append(line)
                    lines.append(line.replace("Unreleased", new_version))
            else:
                lines.append(line)

    with open(changelog_path, mode="wt", encoding="utf-8") as change_log:
        change_log.writelines(lines)
