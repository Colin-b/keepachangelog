import pathlib
from typing import Dict, Optional, Iterable, Union, List, Tuple, Any

from keepachangelog._changelog_dataclasses import Changelog, SemanticVersion, StreamlinesProtocol


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


def to_list(
    changelog_path: Union[str, Iterable[str]], *, show_unreleased: bool = False, reverse: bool = True
) -> List[Tuple[str, dict]]:
    """
    Convert changelog markdown file following keep a changelog format into python list.

    :param changelog_path: Path to the changelog file, or context manager providing iteration on lines.
    :param show_unreleased: Add unreleased section (if any) to the resulting dictionary.
    :param reverse: None: no sort. True: ascending order. False: descending order.
    :return python list of tuples containing version and related changes.
    """
    return _callback_proxy(
        _to_list, changelog_path, show_unreleased=show_unreleased, raw=True, reverse=reverse
    )


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


def _callback_proxy(
    callback: StreamlinesProtocol,
    changelog_path: Union[str, Iterable[str]],
    **kwargs,
) -> Any:
    # Allow for changelog as a file path or as a context manager providing content
    if "\n" in changelog_path:
        return callback(changelog_path, **kwargs)
    path = pathlib.Path(changelog_path)
    with open(path) as change_log:
        return callback(change_log, **kwargs)


def _to_dict(
    change_log: Iterable[str], *, show_unreleased: bool, raw: bool
) -> Dict[str, dict]:
    changelog: Changelog = Changelog()
    changelog.streamlines(change_log)
    changes = changelog.to_dict(show_unreleased=show_unreleased, raw=raw)
    return changes


def _to_list(
    change_log: Iterable[str], *, show_unreleased: bool, raw: bool, reverse: bool
) -> List[Tuple[str, dict]]:
    changelog: Changelog = Changelog()
    changelog.streamlines(change_log)
    changes = changelog.to_list(show_unreleased=show_unreleased, raw=raw, reverse=reverse)
    return changes


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
