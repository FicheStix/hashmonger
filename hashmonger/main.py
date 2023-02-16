"""Main entrypoint for Hashmonger script"""
# hashmonger/main.py

import os
import typer

from rich import print
from rich.prompt import Confirm

app = typer.Typer(
    name = "Hashmonger",
    help = "Hash tool to create hashes from file(s) and/or folder(s)."
)

def main():
    Confirm.get_input(app, "Path to file/folder to be hashed: ", False)

# entrypoint logic
if __name__ == "__main__":
    typer.run(main)