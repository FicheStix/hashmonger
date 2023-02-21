"""Hashmonger entry point."""
# hashmonger/main.py

from pathlib import Path
from typing import Optional

import typer

from hashmonger.hasher import Hasher

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
    print(f"You entered {path}")

if __name__ == "__main__":
    app()