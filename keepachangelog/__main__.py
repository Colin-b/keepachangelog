from typing import List
import argparse

import keepachangelog
from keepachangelog.version import __version__


def _format_change_section(change_type: str, changes: List[str]):
    body = "".join([f"  - {change}\r\n" for change in changes])

    return f"""{change_type.capitalize()}
{body}"""


def _command_show(args):
    output = None

    if args.raw:
        changelog = keepachangelog.to_raw_dict(args.file)
    else:
        changelog = keepachangelog.to_dict(args.file)

    content = changelog.get(args.release)

    if args.raw:
        output = content["raw"]
    else:
        output = "\n".join(
            [
                _format_change_section(change_type, changes)
                for change_type, changes in content.items()
                if change_type != "metadata"
            ]
        )

    print(output)


def _command_release(args):
    new_version = keepachangelog.release(args.file, args.release)

    if new_version:
        print(new_version)


def _parse_args(cmdline: List[str]):
    class CustomFormatter(
        argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
    ):
        pass

    parser = argparse.ArgumentParser(
        prog="keepachangelog",
        description="Manipulate keep a changelog files",
        epilog="""
Examples:

    keepachangelog show 1.0.0
    keepachangelog show 1.0.0 --raw
    keepachangelog show 1.0.0 path/to/CHANGELOG.md

    keepachangelog release
    keepachangelog release 1.0.1
    keepachangelog release 1.0.1 -f path/to/CHANGELOG.md
""",
        formatter_class=CustomFormatter,
    )

    subparser = parser.add_subparsers(title="commands")

    # keepachangelog show
    parser_show_help = "Show the content of a release from the changelog"
    parser_show: argparse.ArgumentParser = subparser.add_parser(
        "show", description=parser_show_help, help=parser_show_help
    )
    parser_show.formatter_class = CustomFormatter

    parser_show.add_argument(
        "release", type=str, help="The version to search in the changelog"
    )
    parser_show.add_argument(
        "file",
        type=str,
        nargs="?",
        default="CHANGELOG.md",
        help="The path to the changelog file",
    )
    parser_show.add_argument(
        "-r", "--raw", action="store_true", help="Show the raw markdown body"
    )

    parser_show.set_defaults(func=_command_show)

    # keepachangelog release
    parser_release_help = "Create a new release in the changelog"
    parser_release: argparse.ArgumentParser = subparser.add_parser(
        "release", description=parser_release_help, help=parser_release_help
    )
    parser_release.formatter_class = CustomFormatter

    parser_release.add_argument(
        "release",
        type=str,
        nargs="?",
        help="The version to add to the changelog. If not provided, a new version will be automatically generated based on the changes in the Unreleased section",
    )
    parser_release.add_argument(
        "-f",
        "--file",
        type=str,
        required=False,
        default="CHANGELOG.md",
        help="The path to the changelog file",
    )

    parser_release.set_defaults(func=_command_release)

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser.parse_args(cmdline)


def main(cmdline: List[str] = None):
    args = _parse_args(cmdline)
    args.func(args)


if __name__ == "__main__":
    main()  # pragma: no cover
