import argparse
import sys

from pyreqmerger.console import console
from pyreqmerger.enums import Errors, MergeMethod
from pyreqmerger.version_file import VersionFile


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyreq",
        description="Merge 2 requirement files into a single file, using the specified method.",
        epilog="Made by https://github.com/mhristodor.",
    )

    vers_file = VersionFile("./version.txt")

    if not vers_file.valid:
        console.print(f"{Errors.INVALID_FILE_PATH}:[red]  {vers_file.path}")
        sys.exit()

    if isinstance(vers_file.version, Errors):
        console.print(f"{vers_file.version}:[red] {vers_file.path}")
        sys.exit()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        default="False",
        help="Displays version then quit",
        version=vers_file.version,
    )

    parser.add_argument(
        "first_req_file",
        type=str,
        action="store",
        help="First file containing requirements",
    )

    parser.add_argument(
        "second_req_file",
        type=str,
        action="store",
        help="Second file containing requirements",
    )

    parser.add_argument(
        "-m",
        "--method",
        required=False,
        action="store",
        choices=list(MergeMethod),
        type=MergeMethod,
        default=MergeMethod.UPGRADE,
        help="Merge method, choose from: 'upgrade' or 'downgrade. (default: upgrade)",
    )

    parser.add_argument(
        "-o",
        "--output",
        required=False,
        action="store",
        type=str,
        default="./merged_requirements.txt",
        help="Output file containing merged requirements. (default: merged_requirements.txt)",
    )
    return parser
