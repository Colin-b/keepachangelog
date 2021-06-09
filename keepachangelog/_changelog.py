import pathlib
import re
from typing import Dict, Optional, Iterable, Union, Tuple, Callable, Any

from keepachangelog._changelog_dataclasses import Changelog, SemanticVersion
from keepachangelog._versioning import to_semantic, InvalidSemanticVersion


def is_release(line: str) -> bool:
    return line.startswith("## ")


def extract_release(line: str) -> Tuple[str, dict]:
    release_line = line[3:].lower().strip(" ")
    # A release is separated by a space between version and release date
    # Release pattern should match lines like: "[0.0.1] - 2020-12-31" or [Unreleased]
    version, release_date = (
        release_line.split(" ", maxsplit=1)
        if " " in release_line
        else (release_line, None)
    )
    version = strip_link(version)

    metadata = {"version": version, "release_date": extract_date(release_date)}
    try:
        metadata["semantic_version"] = to_semantic(version)
    except InvalidSemanticVersion:
        pass

    return version, metadata


def strip_link(value: str) -> str:
    return value.lstrip("[").rstrip("]")


def extract_date(date: str) -> str:
    if not date:
        return date

    return date.lstrip(" -(").rstrip(" )")


def is_category(line: str) -> bool:
    return line.startswith("### ")


def extract_category(line: str) -> str:
    return line[4:].lower().strip(" ")


# Link pattern should match lines like: "[1.2.3]: https://github.com/user/project/releases/tag/v0.0.1"
link_pattern = re.compile(r"^\[(.*)\]: (.*)$")


def is_link(line: str) -> bool:
    return link_pattern.fullmatch(line) is not None


def extract_information(line: str) -> str:
    return line.lstrip(" *-").rstrip(" -")


def to_dict(
    changelog_path: Union[str, Iterable[str]], *, show_unreleased: bool = False
) -> Dict[str, dict]:
    """
    Convert changelog markdown file following keep a changelog format into python dict.

    :param changelog_path: Path to the changelog file, or context manager providing iteration on lines.
    :param show_unreleased: Add unreleased section (if any) to the resulting dictionary.
    :return python dict containing version as key and related changes as value.
    """
    return _callback_proxy(
        _to_dict, changelog_path, show_unreleased=show_unreleased, raw=False
    )


def to_raw_dict(changelog_path: str, *, show_unreleased=False) -> Dict[str, dict]:
    return _callback_proxy(
        _to_dict, changelog_path, show_unreleased=show_unreleased, raw=True
    )


def _callback_proxy(
    callback: Callable[[Iterable[str], ...], Any],
    changelog_path: Union[str, Iterable[str]],
    *args,
    **kwargs,
) -> Any:
    # Allow for changelog as a file path or as a context manager providing content
    if "\n" in changelog_path:
        return callback(changelog_path, *args, **kwargs)
    path = pathlib.Path(changelog_path)
    with open(path) as change_log:
        return callback(change_log, *args, **kwargs)


def _to_dict(
    change_log: Iterable[str], *, show_unreleased: bool, raw: bool
) -> Dict[str, dict]:
    changelog: Changelog = Changelog()
    changelog.streamlines(change_log)
    changes = changelog.to_dict(show_unreleased=show_unreleased, raw=raw)
    return changes


def from_dict(changes: Dict[str, dict]) -> str:
    header = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n"""

    changelog: Changelog = Changelog(header=header.splitlines(), changes=changes)
    return changelog.to_markdown()


def release(changelog_path: str, new_version: str = None) -> Optional[str]:
    """
    Release a new version based on changelog unreleased content.

    :param changelog_path: Path to the changelog file.
    :param new_version: The new version to use instead of trying to guess one.
    :return: The new version, None if there was no change to release.
    """
    changelog: Changelog = Changelog()
    _callback_proxy(changelog.streamlines, changelog_path)
    success = _release_version(changelog_path, changelog, new_version)
    if success:
        return changelog.current_version_string


def _release_version(
    changelog_path: str,
    changelog: Changelog,
    new_version: Optional[SemanticVersion] = None,
) -> bool:
    success = changelog.release(new_version)
    if success:
        with open(changelog_path, "wt") as change_log:
            change_log.writelines(changelog.to_markdown(raw=True))
    return success
