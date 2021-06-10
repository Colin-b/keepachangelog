import re
import string
from dataclasses import dataclass, field, fields
from datetime import date, datetime
from typing import (
    List,
    Optional,
    Tuple,
    Any,
    Dict,
    Callable,
    Generator,
    Iterable,
    Union,
)

from keepachangelog._versioning import (
    InvalidSemanticVersion,
    UnmatchingSemanticVersion,
)

DictFactoryCallable = Callable[[List[Tuple[str, Any]]], Dict[str, Any]]
UNRELEASED = "unreleased"

RE_URL = re.compile(r"^.*/(?P<current_tag>.*)\.\.\.(?P<un_tag>\w*).*$", re.DOTALL)
# Link pattern should match lines like: "[1.2.3]: https://github.com/user/project/releases/tag/v0.0.1"
RE_LINK_LINE = re.compile(r"^\[(?P<version>.*)\]: (?P<url>.*)$")
RE_SEMVER = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:[-\.]?(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def is_release(line: str) -> bool:
    return line.startswith("## ")


def is_category(line: str) -> bool:
    return line.startswith("### ")


def matches_link(line: str) -> re.Match:
    return RE_LINK_LINE.fullmatch(line)


@dataclass(eq=True, order=True)
class SemanticVersion:
    major: int = field(compare=True)
    minor: int = field(compare=True)
    patch: int = field(compare=True)
    __prerelease: Optional[str] = field(default=None, compare=False)
    __prerelease_cmp: str = field(default="1", compare=True)
    buildmetadata: Optional[str] = field(default=None, compare=False)

    @property
    def prerelease(self):
        return self.__prerelease

    @prerelease.setter
    def prerelease(self, value):
        self.__prerelease = value
        self.__prerelease_cmp = "1" if value is None else f"0{self.__prerelease}"

    @classmethod
    def to_semantic(cls, version: Optional[str] = "") -> dict:
        if not version:
            return cls.initial_version().to_dict(force=True)
        match = RE_SEMVER.fullmatch(version)
        if match:
            return {
                key: int(value) if key in ("major", "minor", "patch") else value
                for key, value in match.groupdict().items()
            }

        raise InvalidSemanticVersion(version)

    @classmethod
    def initial_version(cls):
        return cls.from_version_string("0.0.0")

    @classmethod
    def from_version_string(cls, version_string: str) -> "SemanticVersion":
        semver = cls.to_semantic(version_string)
        return cls.from_dict(semver)

    @classmethod
    def from_dict(cls, data: dict):
        prerelease = data.pop("prerelease")
        obj = cls(**data)
        obj.prerelease = prerelease
        return obj

    def bump_major(self):
        return self.__class__.from_dict(
            self.to_dict(force=True)
            | SemanticVersion(self.major + 1, 0, 0).to_dict(force=True)
        )

    def bump_minor(self):
        return self.__class__.from_dict(
            self.to_dict(force=True)
            | SemanticVersion(self.major, self.minor + 1, 0).to_dict(force=True)
        )

    def bump_patch(self):
        return self.__class__.from_dict(
            self.to_dict(force=True)
            | SemanticVersion(self.major, self.minor, self.patch + 1).to_dict(
                force=True
            )
        )

    def release_version(self):
        return self.__class__.from_dict(
            self.to_dict(force=True)
            | SemanticVersion(self.major, self.minor, self.patch).to_dict(force=True)
        )

    def to_tuple(self) -> Tuple[int, int, int, Optional[str], Optional[str]]:
        return self.major, self.minor, self.patch, self.prerelease, self.buildmetadata

    def to_dict(self, *, force=False) -> Optional[Dict]:
        if self.to_tuple() == (0, 0, 0, None, None) and not force:
            return
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "prerelease": self.prerelease,
            "buildmetadata": self.buildmetadata,
        }

    def __str__(self):
        return (
            f"{self.major}.{self.minor}.{self.patch}"
            f"{f'-{self.prerelease}' if self.prerelease is not None else ''}"
            f"{f'+{self.buildmetadata}' if self.buildmetadata is not None else ''}"
        )


@dataclass
class Metadata:
    __RE_RELEASE = re.compile(
        r"^## (?:\[(?P<name>.*)]|\[(?P<version>.*)] - (?P<raw_date>(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})))\s*$"
    )
    version: str = UNRELEASED
    release_date: Optional[date] = None
    raw_release_date: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.release_date, str):
            self.raw_release_date = self.release_date
            self.release_date = None
        if self.raw_release_date is not None and self.release_date is None:
            self.release_date = self.parse_date(self.raw_release_date)

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

    @property
    def semantic_version_strict(self) -> SemanticVersion:
        try:
            return SemanticVersion.from_version_string(self.version)
        except InvalidSemanticVersion:
            return SemanticVersion(0, 0, -1)

    def to_dict(self, *, raw: bool = False) -> dict:
        out = {
            "version": self.version.lower(),
        }
        if self.is_released:
            if raw and self.raw_release_date is not None:
                out["release_date"] = self.raw_release_date
            elif self.release_date is not None:
                out["release_date"] = self.release_date.strftime("%Y-%m-%d")
        if self.is_named_version:
            out["release_date"] = None
        if self.version.strip() and self.semantic_version is not None:
            out["semantic_version"] = self.semantic_version.to_dict()
        if self.url is not None:
            out["url"] = self.url
        return out

    @staticmethod
    def parse_date(datestring: str) -> date:
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
        for accepted_format in accepted_formats:
            try:
                dateobj = datetime.strptime(datestring, accepted_format).date()
            except ValueError:
                pass
            else:
                break
        else:
            dateobj = datestring
        return dateobj

    def parse_release_line_best_effort(self, line: str) -> None:
        """
        ## [1.0.1] - May 01, 2018
        ## 1.0.0 (2017-01-01)
        """
        version, *datelist = line[3:].strip().split(maxsplit=1)
        self.version = version.strip(string.punctuation + string.whitespace)
        if datelist:
            self.raw_release_date = datelist.pop().strip(
                string.punctuation + string.whitespace
            )
            release_date = self.parse_date(self.raw_release_date)
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
            self.raw_release_date = groups["raw_date"]
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

    def to_markdown(self, *, bullet: str = "-") -> str:
        return "\n".join(f"{bullet} {note}" for note in self)


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
            if "semantic_version" in self.metadata:
                semver = SemanticVersion.from_dict(self.metadata["semantic_version"])
                if "version" in self.metadata:
                    semver2 = SemanticVersion.from_version_string(
                        self.metadata["version"]
                    )
                    # to_tuple() because we want them to be exactly equal, even buildmetadata
                    if semver.to_tuple() != semver2.to_tuple():
                        raise UnmatchingSemanticVersion(
                            self.metadata["version"], self.metadata["semantic_version"]
                        )
                else:
                    self.metadata["version"] = str(semver)
                self.metadata.pop("semantic_version")
            self.metadata = Metadata(**self.metadata)
        for f in fields(self):
            if f.type is not Category:
                continue
            category = getattr(self, f.name)
            if isinstance(category, list) and not isinstance(category, Category):
                setattr(self, f.name, Category(category))

    @property
    def is_released(self):
        return self.metadata.is_released

    @property
    def contains_breaking_changes(self) -> bool:
        return bool(self.removed) or bool(self.changed)

    @property
    def contains_only_bug_fixes(self):
        return all(
            [
                self.fixed,
                not self.uncategorized,
                not self.changed,
                not self.added,
                not self.security,
                not self.deprecated,
                not self.removed,
            ]
        )

    @property
    def is_empty(self):
        return all(
            [
                not self.fixed,
                not self.uncategorized,
                not self.changed,
                not self.added,
                not self.security,
                not self.deprecated,
                not self.removed,
            ]
        )

    def to_markdown(self, *, raw=False) -> str:
        if raw:
            return "\n".join(self.__lines)
        out = []
        if self.uncategorized:
            out.append(self.uncategorized.to_markdown(bullet="*"))
            out.append("")
        for f in fields(self):
            if f.type is Category and f.name != "uncategorized":
                category: Category = getattr(self, f.name)
                if category:
                    out.append(f"### {f.name.capitalize()}")
                    out.append(category.to_markdown())
                    out.append("")
        return "\n".join(out)

    def to_dict(self, *, raw=False) -> dict:
        out = {"metadata": self.metadata.to_dict(raw=raw)}
        if raw:
            if self.__lines:
                out["raw"] = "\n".join(self.__lines)
                if not out["raw"].endswith("\n"):
                    out["raw"] += "\n"
        else:
            for f in fields(self):
                if f.type is Category:
                    category = getattr(self, f.name)
                    if category:
                        out[f.name] = category
        return out

    def parse_category_line(self, line: str):
        category = line[4:].lower().strip(" ")
        if hasattr(self, category):
            self.__active_category = getattr(self, category)

    def streamline(self, line: str):
        if is_release(line):
            self.metadata.parse_release_line(line)
            return
        self.__lines.append(line)
        if is_category(line):
            self.parse_category_line(line)
        else:
            self.__active_category.streamline(line)


@dataclass
class Changelog:
    header: List[str] = field(default_factory=list)
    changes: Dict[str, Change] = field(default_factory=dict)

    @property
    def current_version(self) -> Union[SemanticVersion, str]:
        maxver = self.__latest_version()
        return (
            (maxver["semver"] or maxver["version"])
            if maxver["is_released"]
            else maxver["semver_s"]
        )

    @property
    def current_version_string(self) -> str:
        maxver = self.__latest_version()
        return maxver["version"]

    def __latest_version(self) -> dict:
        return max(
            (
                {
                    "semver": change.metadata.semantic_version,
                    "semver_s": change.metadata.semantic_version_strict,
                    "version": change.metadata.version,
                    "is_released": change.is_released,
                }
                for change in self.changes.values()
            ),
            key=lambda version: (version["is_released"], version["semver_s"]),
        )

    @property
    def next_version(self) -> SemanticVersion:
        current = self.current_version
        if current.prerelease is not None:
            return current.release_version()
        unreleased_change = self.unreleased_unique
        if (
            len(self.changes) == 1
            and unreleased_change is list(self.changes.values())[0]
        ):
            current = SemanticVersion.initial_version()
        if unreleased_change.contains_breaking_changes:
            return current.bump_major()
        if unreleased_change.contains_only_bug_fixes:
            return current.bump_patch()
        return current.bump_minor()

    @property
    def unreleased(self) -> List[Change]:
        unreleased_changes = []
        for change in self.changes.values():
            if not change.is_released:
                unreleased_changes.append(change)
        return unreleased_changes

    @property
    def unreleased_unique(self) -> Change:
        unreleased_changes = self.unreleased
        if len(unreleased_changes) > 1:
            raise AttributeError("There are several unreleased sections!")
        return unreleased_changes.pop() if unreleased_changes else Change()

    @property
    def sorted_changes(self) -> Generator[Tuple[str, Change], None, None]:
        for version, change in self.changes.items():
            if not change.is_released:
                yield version, change
        released = ((v, c) for v, c in self.changes.items() if c.is_released)
        yield from sorted(
            released, key=lambda k: k[1].metadata.semantic_version_strict, reverse=True
        )

    def release(self, new_version: Optional[SemanticVersion] = None) -> bool:
        unreleased_change = self.unreleased_unique
        if unreleased_change.is_empty:
            return False
        current_version = self.current_version
        if isinstance(current_version, str):
            raise InvalidSemanticVersion(current_version)
        if new_version is None:
            new_version = self.next_version
        return self.__release_unreleased_change(
            unreleased_change, current_version, new_version
        )

    def __release_unreleased_change(
        self,
        unreleased: Change,
        current_version: SemanticVersion,
        new_version: SemanticVersion,
    ) -> bool:
        self.wipe_unreleased_references()
        un_metadata = unreleased.metadata
        un_metadata.version = str(new_version)
        un_metadata.release_date = date.today()
        old_url = un_metadata.url
        self.__update_url(unreleased, current_version, new_version)
        self.changes[str(new_version)] = unreleased

        if old_url is not None:
            self.unreleased_unique.metadata.url = old_url.replace(
                str(current_version), str(new_version)
            )
        return True

    @staticmethod
    def __update_url(
        change: Change,
        current_version: SemanticVersion,
        new_version: SemanticVersion,
    ) -> None:
        old_url = change.metadata.url
        if old_url is not None:
            match_old_url = RE_URL.fullmatch(old_url)
            if match_old_url is not None:
                groups = match_old_url.groupdict()
                current_tag = groups["current_tag"]
                new_tag = current_tag.replace(str(current_version), str(new_version))
                released_url = old_url.replace(groups["un_tag"], new_tag)
                change.metadata.url = released_url

    def wipe_unreleased_references(self) -> None:
        """Wipe all information from unreleased versions."""
        for version in self.changes.keys():
            if not self.changes[version].is_released:
                self.changes[version] = Change(metadata=Metadata(version=version))

    def __post_init__(self):
        self.__active_change: Optional[Change] = None
        temp_changes = {}
        for key, change in self.changes.items():
            if isinstance(change, dict):
                temp_changes[key] = Change(**change)
        self.changes = temp_changes

    def links(self) -> Generator[List[Tuple[str, str]], None, None]:
        for version, change in self.sorted_changes:
            yield version, change.metadata.url

    def to_markdown(self, *, raw=False) -> str:
        out = self.header[:]
        if not raw:
            out.append("")
        for version, change in self.sorted_changes:
            if change.metadata.release_date is not None:
                out.append(
                    f"## [{version.capitalize()}] - {change.metadata.release_date}"
                )
            else:
                out.append(f"## [{version.capitalize()}]")
            change_md = change.to_markdown(raw=raw)
            if change_md or not change.is_released:
                out.append(change_md)
        out += [
            f"[{v.capitalize()}]: {link}"
            for v, link in self.links()
            if link is not None
        ]
        out.append("")
        return "\n".join(out)

    def to_dict(self, *, show_unreleased: bool = False, raw: bool = False):
        return {
            version.lower(): change.to_dict(raw=raw)
            for version, change in self.changes.items()
            if change.is_released or show_unreleased
        }

    def streamlines(self, lines: Iterable[str]):
        for line in lines:
            line = line.strip("\n")
            self.streamline(line)

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
        elif self.__active_change is not None:
            self.__active_change.streamline(line)
        else:
            self.header.append(line)
