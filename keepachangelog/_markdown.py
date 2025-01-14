import re

# Link pattern should match lines like: "[1.2.3]: https://github.com/user/project/releases/tag/v0.0.1"
link_pattern = re.compile(r"^\[(.*)\]: (.*)\n$")


def is_heading(line: str, heading_level: int) -> bool:
    return line.lstrip(" ").startswith(f"{'#' * heading_level} ")


def from_heading(line: str, heading_level: int) -> str:
    return line.lstrip(" ")[heading_level:].strip(" \n")


def unlink(value: str) -> str:
    return value.lstrip("[").rstrip("]")


def is_link(line: str) -> bool:
    return link_pattern.fullmatch(line.lstrip(" ")) is not None


def unlist(line: str) -> str:
    line = line.lstrip(" ")
    if line and line[0] in "-*+":
        list_line = line[1:]
        # Empty list item
        if not list_line:
            return ""
        # List item
        if list_line[0] == " ":
            return list_line[1:]
    # Non list item (can start with a list identifier)
    return line
