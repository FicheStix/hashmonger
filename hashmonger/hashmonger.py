"""Main entrypoint for Hashmonger script"""
# hashmonger/main.py

import os.path
import typer
import hashlib
import io

from typing import Optional
from rich import print

__version__ = "0.1.1"

def version_callback(value: Optional[bool]):
    if value:
        print(f"You are using Hashmonger version {__version__}")
        raise typer.Exit()

def get_item_type(item_path: str) -> Optional[str]:
    """
    Checks if the supplied path is to a real folder or file. 
    If not valid, program exits. Only works for files at this time.
    """
   
    if os.path.exists(item_path):
        if os.path.isfile(item_path):
            return "file"
        elif os.path.isdir(item_path):
            return "dir"
        else:
            raise typer.Exit()
    raise typer.Exit()

def get_hashes(item_path: str) -> dict:
    BUFFER = io.DEFAULT_BUFFER_SIZE
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()

    hash_dict = {
        "sha1": sha1,
        "sha256": sha256,
        "md5": md5
    }

    # if we're hashing a file open it and begin reading bytes into the hash objects
    with open(item_path, "rb") as binary_reader:
        # update all hash opbjects in the hash dictionary with bytes read from file
        while True:
            read_buffer = binary_reader.read(BUFFER)

            if len(read_buffer) == 0:
                break
            
            for hash_type in hash_dict:
                hash_dict[hash_type].update(read_buffer)

        # update read_buffer with how many bytes were read
        bytes_read = len(read_buffer)

    return hash_dict

def main(item_path: str = typer.Option(..., "--path", "-p", help="File or folder path to be hashed", prompt="Path (file or folder)", show_default=False),
         hash_type: str = typer.Option(None, "--hash", "-d", help="Single digest or a comma separated list of digests", show_default=False),
         version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True)
):
    """Compute file/folder hashes."""

    item_type = get_item_type(item_path)

    if item_type == "file":
        hashes = get_hashes(item_path)
        for hash in hashes:
            print(f"{hash}\t\t{hashes[hash].hexdigest()}")
    elif item_type == "dir":
        print("Directory")


# entrypoint logic
if __name__ == "__main__":
    typer.run(main)