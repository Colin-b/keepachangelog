import dataclasses
import re
import string
from dataclasses import dataclass, field, fields
from datetime import date, datetime
from typing import List, Optional, Tuple, Any, Dict, Callable

from keepachangelog._versioning import to_semantic, InvalidSemanticVersion

DictFactoryCallable = Callable[[List[Tuple[str, Any]]], Dict[str, Any]]
UNRELEASED = "unreleased"


def is_release(line: str) -> bool:
    return line.startswith("## ")


def is_category(line: str) -> bool:
    return line.startswith("### ")


# Link pattern should match lines like: "[1.2.3]: https://github.com/user/project/releases/tag/v0.0.1"
link_pattern = re.compile(r"^\[(?P<version>.*)\]: (?P<url>.*)$")


def matches_link(line: str) -> re.Match:
    return link_pattern.fullmatch(line)


@dataclass
class SemanticVersion:
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    buildmetadata: Optional[str] = None

    @classmethod
    def from_version_string(cls, version_string: str) -> "SemanticVersion":
        return cls(**to_semantic(version_string))

    def to_tuple(self) -> Tuple[int, int, int, Optional[str], Optional[str]]:
        return self.major, self.minor, self.patch, self.prerelease, self.buildmetadata

    def to_dict(self) -> Optional[Dict]:
        if self.to_tuple() == (0, 0, 0, None, None):
            return
        return dataclasses.asdict(self)


@dataclass
class Metadata:
    __RE_RELEASE = re.compile(
        r"^## (?:\[(?P<name>.*)]|\[(?P<version>.*)] - (?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}))\s*$"
    )
    version: str = UNRELEASED
    release_date: Optional[date] = None
    url: Optional[str] = None

    @property
    def is_released(self):
        return not self.version.lower() == UNRELEASED and (
            self.release_date is not None or self.url is not None
        )

    @property
    def is_named_version(self):
        return self.version and not self.semantic_version

    @property
    def semantic_version(self) -> Optional[SemanticVersion]:
        try:
            return SemanticVersion.from_version_string(self.version)
        except InvalidSemanticVersion:
            return None

    def to_dict(self) -> dict:
        out = {
            "version": self.version.lower(),
        }
        if self.is_released:
            if self.release_date is not None:
                out["release_date"] = self.release_date.strftime("%Y-%m-%d")
        if self.is_named_version:
            out["release_date"] = None
        if self.version.strip() and self.semantic_version is not None:
            out["semantic_version"] = self.semantic_version.to_dict()
        if self.url is not None:
            out["url"] = self.url
        return out

    def parse_release_line_best_effort(self, line: str) -> None:
        """
        ## [1.0.1] - May 01, 2018
        ## 1.0.0 (2017-01-01)
        """
        accepted_formats = [
            "%Y-%m-%d",  # 2020-10-09
            "%d-%m-%Y",  # 09-10-2020
            "%Y/%m/%d",  # 2020/10/09
            "%d/%m/%Y",  # 09/10/2020
            "%b %d, %Y",  # Oct 9, 2020
            "%B %d, %Y",  # October 9, 2020
            "%b %d %Y",  # Oct 9 2020
            "%B %d %Y",  # October 9 2020
        ]
        version, *datelist = line[3:].strip().split(maxsplit=1)
        self.version = version.strip(string.punctuation + string.whitespace)
        if datelist:
            datestring = datelist.pop().strip(string.punctuation + string.whitespace)
            for accepted_format in accepted_formats:
                try:
                    release_date = datetime.strptime(datestring, accepted_format).date()
                except ValueError:
                    pass
                else:
                    break
            else:
                release_date = datestring
        else:
            release_date = None
        self.release_date = release_date

    def parse_release_line(self, line: str) -> None:
        match = self.__RE_RELEASE.match(line)
        if match is None:
            return self.parse_release_line_best_effort(line)
        groups = match.groupdict()
        has_version: bool = groups["version"] is not None
        if has_version:
            self.version = groups["version"]
            self.release_date = date(
                int(groups["year"]), int(groups["month"]), int(groups["day"])
            )
        else:
            self.version = groups["name"]

    @classmethod
    def from_release_line(cls, line: str) -> "Metadata":
        obj = cls()
        obj.parse_release_line(line)
        return obj


Note = str


class Category(List[Note]):
    @staticmethod
    def extract_information(line: str) -> str:
        return line.lstrip(" *-").rstrip(" -")

    def streamline(self, line: str):
        note: Note = Note(self.extract_information(line))
        if note:
            self.append(note)


@dataclass
class Change:
    metadata: Metadata = field(default_factory=Metadata)
    uncategorized: Category = field(default_factory=Category)
    changed: Category = field(default_factory=Category)
    added: Category = field(default_factory=Category)
    fixed: Category = field(default_factory=Category)
    security: Category = field(default_factory=Category)
    deprecated: Category = field(default_factory=Category)
    removed: Category = field(default_factory=Category)

    def __post_init__(self):
        self.__lines: List[str] = []
        self.__active_category: Optional[Category] = self.uncategorized
        if isinstance(self.metadata, dict):
            self.metadata = Metadata(**self.metadata)
        for f in fields(self):
            if f.type is not Category:
                continue
            if isinstance(getattr(self, f.name), dict):
                setattr(self, f.name, Category(**getattr(self, f.name)))

    @property
    def is_released(self):
        return self.metadata.is_released

    def to_dict(self) -> dict:
        out = {"metadata": self.metadata.to_dict()}
        for f in fields(self):
            if f.type is Category:
                category = getattr(self, f.name)
                if category:
                    out[f.name] = getattr(self, f.name)
        return out

    def parse_category_line(self, line: str):
        category = line[4:].lower().strip(" ")
        if hasattr(self, category):
            self.__active_category = getattr(self, category)

    def streamline(self, line: str):
        self.__lines.append(line)
        if is_release(line):
            self.metadata.parse_release_line(line)
        elif is_category(line):
            self.parse_category_line(line)
        else:
            self.__active_category.streamline(line)


@dataclass
class Changelog:
    header: List[str] = field(default_factory=list)
    changes: Dict[str, Change] = field(default_factory=dict)

    def __post_init__(self):
        self.__active_change: Optional[Change] = None
        temp_changes = {}
        for key, change in self.changes.items():
            if isinstance(change, dict):
                temp_changes[key] = Change(**change)
        self.changes = temp_changes

    def to_dict(self, *, show_unreleased: bool = False):
        return {
            version.lower(): change.to_dict()
            for version, change in self.changes.items()
            if change.is_released or show_unreleased
        }

    def streamline(self, line: str):
        link_match = matches_link(line)
        if link_match is not None:
            groups = link_match.groupdict()
            self.changes.setdefault(
                groups["version"], Change(Metadata(version=groups["version"]))
            ).metadata.url = groups["url"]
            return
        if is_release(line):
            self.__active_change = Change()
            self.__active_change.streamline(line)
            self.changes[self.__active_change.metadata.version] = self.__active_change
        if self.__active_change is not None:
            self.__active_change.streamline(line)
        else:
            self.header.append(line)
