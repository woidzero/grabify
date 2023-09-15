"""
Grabify
~~~~~~~~~~~~~~~~~~~

🎼 A command-line tool that allows you to download artwork and metadata from Spotify 
tracks and albums without authentication.

:copyright: (c) 2023 woidzero
:license: MIT, see LICENSE for more details.
"""
import sys

import click

from .cli import COMMANDS, grabify

for cmd in COMMANDS:
    grabify.add_command(cmd)


def main() -> click.Group:
    """Entry point for grabify."""
    return grabify()


if __name__ == "__main__":
    sys.exit(main())  # type: ignore
