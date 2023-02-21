"""Main entrypoint for Hashmonger script"""
# hashmonger/main.py

import os.path
import typer
import hashlib
import io

from pathlib import Path
from typing import Optional
from hashmonger import __app_name__, __version__

class Hasher:
    """
    Hasher class returns an object that exposes various hash methods. When
    called, these hash read chunks of the given file path and returns a
    hash digest.
    """

    def __init__(self, path: str):
        self.file_path = path

    def get_path_type(self) -> Optional[str]:
        """
        Validates a given file/folder path and returns whether
        the path leads to a file or folder. 
        """
        path_is_file = Path.is_file(self.file_path)
        path_is_dir = Path.is_dir(self.file_path)

        if path_is_file:
            return "File"
        elif path_is_dir:
            return "Folder"
        else:
            return None


def get_hashes(item_path: str) -> dict:
    BUFFER = io.DEFAULT_BUFFER_SIZE
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()

    hash_dict = {
        "SHA256": sha256,
        "SHA1": sha1,
        "MD5": md5
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

    """Compute file/folder hashes."""
    try:
        item_type = get_item_type(item_path)
    except ValueError:
        print("The path you provided is not valid.\nEnd of line.")
        raise typer.Exit()

    if item_type == "file":
        hashes = get_hashes(item_path)
        for hash in hashes:
            print(f"{hash}\t\t{hashes[hash].hexdigest()}")
    elif item_type == "dir":
        print("Directory")


