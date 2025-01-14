import re

# Link pattern should match lines like: "[1.2.3]: https://github.com/user/project/releases/tag/v0.0.1"
link_pattern = re.compile(r"^\[(.*)\]: (.*)$")


def is_heading(line: str, heading_level: int) -> bool:
    return line.startswith(f"{'#' * heading_level} ")


def unlink(value: str) -> str:
    return value.lstrip("[").rstrip("]")


def is_link(line: str) -> bool:
    return link_pattern.fullmatch(line) is not None
