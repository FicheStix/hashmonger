"""Hashmonger entry point."""
# hashmonger/main.py

from pathlib import Path
from typing import Optional

import typer

from hsh import __app_name__, __version__
from hsh.hasher import Hasher


app = typer.Typer(
    name=__app_name__,
    add_completion=False,
    pretty_exceptions_enable=False,
    no_args_is_help=True,
    help="Hashmonger is a simple tool to compute file hashes."
)

def validate_path(item_path: str):
    if not Path(item_path).exists():
        print("The item path supplied does not exist.")
        raise typer.Exit()
    return item_path


def show_version(show: bool):
    if show:
        print(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.command()
def gethash(
    path: Path = typer.Argument(
        ...,
        help="Path to existing file. If path is a directory, files within are hashed.",
        show_default=False,
        callback=validate_path
    ),
    sha256: bool = typer.Option(
        False,
        "--sha256", 
        is_flag=True,
        help="Flag. Only display SHA256 hash digest."
    ),
    sha1: bool = typer.Option(
        False,
        "--sha1", 
        is_flag=True,
        help="Flag. Only display SHA1 hash digest."
    ),
    md5: bool = typer.Option(
        False,
        "--md5", 
        is_flag=True,
        help="Flag. Only display MD5 hash digest."
    ),
):
    """
    Compute hashes for existing file(s).
    """
    hashes = Hasher(path)
    hash_list = hashes.get_hashes()

    if sha256:
        sha256_digest(hash_list)
    elif sha1:
        sha1_digest(hash_list)
    elif md5:
        md5_digest(hash_list)
    else:
        all_digests(hash_list)


def sha256_digest(hash_list: dict):
    print(f"SHA256:\t{hash_list['SHA256'].hexdigest()}")


def sha1_digest(hash_list: dict):
    print(f"SHA1\t{hash_list['SHA1'].hexdigest()}")


def md5_digest(hash_list: dict):
    print(f"MD5\t{hash_list['MD5'].hexdigest()}")


def all_digests(hash_list: dict):
    for hash in hash_list:
        print(f"{hash}\t{hash_list[hash].hexdigest()}")


@app.callback()
def version_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=show_version,
        is_eager=True
    )
):
    """
    Show current application version.
    """

if __name__ == "__main__":
    app()