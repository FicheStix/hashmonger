"""Main entrypoint for Hashmonger script"""
# hashmonger/main.py

import os
import typer

from typing import Optional

__version__ = "0.1.0"

def version_callback(value: Optional[bool]):
    if value:
        print(f"You are using Hashmonger version {__version__}")
        raise typer.Exit()

def main(item_path: str = typer.Option(..., "--path", "-p", help="File or folder path to be hashed", prompt="File/folder path", show_default=False),
         digest: str = typer.Option("sha256","--digest", "-d", help="Single digest or a comma separated list of digests"),
         version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True)
):
    """Compute file/folder hashes."""

    if item_path is None:
        print(f"Please specify a file or folder to hash.")
        raise typer.Exit()
    else:
        print(f"You entered: {item_path}")

# entrypoint logic
if __name__ == "__main__":
    typer.run(main)