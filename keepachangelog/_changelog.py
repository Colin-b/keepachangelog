import datetime
import re
from pathlib import Path
from typing import Optional, Union

from keepachangelog._markdown import (
    is_heading,
    is_link,
    unlink,
    link_pattern,
    from_heading,
    unlist,
)
from keepachangelog._versioning import (
    actual_version,
    guess_unreleased_version,
    to_semantic,
    InvalidSemanticVersion,
    VersionAlreadyReleasedError,
)


def is_release(line: str) -> bool:
    return is_heading(line, heading_level=2)


def from_release(line: str) -> str:
    return from_heading(line, heading_level=2)


def add_release(changes: dict[str, dict], line: str) -> dict:
    release_line = from_release(line).lower()
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


def extract_date(date: str) -> str:
    if not date:
        return date

    return date.lstrip(" -(").rstrip(" )")


def to_dict(
    changelog_path: Union[str, Path], *, show_unreleased: bool = False
) -> dict[str, dict]:
    """
    Convert changelog markdown file following keep a changelog format into python dict.

    :param changelog_path: Path to the changelog file.
    :param show_unreleased: Add unreleased section (if any) to the resulting dictionary.
    :return python dict containing version as key and related changes as value.
    """
    changes = to_raw_dict(changelog_path, show_unreleased=show_unreleased)

    for version, current_release in changes.items():
        if raw_release := current_release.pop("raw", None):
            current_release.update(_release_to_dict(raw_release))

    return changes


def is_category(line: str) -> bool:
    return is_heading(line, heading_level=3)


def from_category(line: str) -> str:
    return from_heading(line, heading_level=3)


def _release_to_dict(markdown_release: str) -> dict:
    category = []
    category_indent = None
    _release = {"uncategorized": category}

    for line in markdown_release.splitlines():
        if is_category(line):
            category_name = from_category(line).lower()
            category_indent = None
            category = _release.setdefault(category_name, [])
        else:
            line_indent = len(line) - len(line.lstrip(" "))
            if category_indent is None:
                category_indent = line_indent

            if line_indent > category_indent:
                category[-1] += f"\n{line[category_indent:].strip(' ')}"
            else:
                if clean_line := unlist(line[line_indent:]).strip(" "):
                    category.append(clean_line)

    # Avoid empty uncategorized
    if not _release["uncategorized"]:
        _release.pop("uncategorized", None)

    return _release


def from_dict(changes: dict[str, dict]) -> str:
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


def to_raw_dict(
    changelog_path: Union[str, Path], *, show_unreleased: bool = False
) -> dict[str, dict]:
    """
    Convert changelog markdown file following keep a changelog format into python dict.

    :param changelog_path: Path to the changelog file.
    :param show_unreleased: Add unreleased section (if any) to the resulting dictionary.
    :return python dict containing version as key and related changes as value.
    """
    changes = {}
    # As URLs can be defined before actual usage, maintain a separate dict
    urls = {}
    with open(changelog_path, encoding="utf-8") as change_log:
        current_release = {}
        for line in change_log:
            if is_release(line):
                current_release = add_release(changes, line)
            elif is_link(line):
                link_match = link_pattern.fullmatch(line)
                urls[link_match.group(1).lower()] = link_match.group(2)
            elif line.strip(" \n"):
                current_release["raw"] = current_release.get("raw", "") + line

    # Add url for each version (create version if not existing)
    for version, url in urls.items():
        changes.setdefault(version, {"metadata": {"version": version}})["metadata"][
            "url"
        ] = url

    unreleased_version = None
    for version, current_release in changes.items():
        metadata = current_release["metadata"]
        # If there is an empty release date, it identifies the unreleased section
        if ("release_date" in metadata) and not metadata["release_date"]:
            unreleased_version = version

    if not show_unreleased:
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
    if new_version:
        if new_version in changelog.keys():
            raise VersionAlreadyReleasedError(new_version)
    else:
        new_version = guess_unreleased_version(changelog, current_semantic_version)
    if new_version:
        release_version(changelog_path, current_version, new_version)
    return new_version


def release_version(
    changelog_path: str, current_version: Optional[str], new_version: str
) -> None:
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
