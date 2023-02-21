"""Hashmonger entry point."""
# hashmonger/main.py

from pathlib import Path
from typing import Optional

import typer

import hashmonger.hasher as hasher

from . import __app_name__, __version__

app = typer.Typer()

def validpath_callback(value: Path):
    if not value.exists():
        raise typer.BadParameter("Item path not valid.")
    return value

@app.callback()
def help():
    """
    Hashmonger is a simple CLI that will compute various hash digests
    for a given file. Currently supports hashing a single file at a time.
    """

@app.command()
def hash(path: Path = typer.Option(..., callback=validpath_callback)):
    """
    Return hash digest(s) for given item path.
    """
    hashes = hasher.Hasher(path)
    hash_list = hashes.get_hashes()
    for hash in hash_list:
         print(f"{hash}\t\t{hash_list[hash].hexdigest()}")

@app.command()
def version():
    """
    Displays current version of application.
    """
    print(f"{__app_name__} {__version__}")

if __name__ == "__main__":
    app()