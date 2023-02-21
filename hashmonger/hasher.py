"""Main entrypoint for Hashmonger script"""
# hashmonger/main.py

import hashlib
import io
from pathlib import Path
from typing import Optional


class Hasher:
    """
    Hasher class returns an object that exposes various hash methods. When
    called, these hash read chunks of the given file path and returns a
    hash digest.
    """

    def __init__(self, path: str):
        self.item_path = self._validate_path(path)
        self.item_type = self._get_path_type(self.item_path)
        self.buffer_size = io.DEFAULT_BUFFER_SIZE
        
        _sha1_hash = hashlib.sha1()
        _sha256_hash = hashlib.sha256()
        _md5_hash = hashlib.md5()

        self.hashes = {
            "SHA256": _sha256_hash,
            "SHA1": _sha1_hash,
            "MD5": _md5_hash
        }

    def _validate_path(self, item_path: str) -> str:
        if Path(item_path).exists():
            return item_path
        else:
            raise FileNotFoundError("The path provided does not exist.")
        
    def _get_path_type(self, item_path: str) -> Optional[str]:
        """
        Validates a given file/folder path and returns whether
        the path leads to a file or folder. 
        """
        path_is_file = Path(item_path).is_file()
        path_is_dir = Path(item_path).is_dir()

        if path_is_file:
            return "File"
        elif path_is_dir:
            return "Folder"
        else:
            return None

    def list_hash_types(self, hashes: dict):
        print("The following hash types are currently supported:\n")
        for hashtype in hashes:
            print(f"\n{hashtype}")

    def get_hashes(self) -> dict:
        """
        Computes hashes for given has type and item path.
        This is a 'private' method and expects a vetted item path.
        """
        with open(self.item_path, "rb") as binary_reader:
            while True:
                read_buffer = binary_reader.read(self.buffer_size)
                if len(read_buffer) == 0:
                    break
                # update all hash objects in the hash dictionary 
                # with bytes read from file
                for hash_type in self.hashes:
                    self.hashes[hash_type].update(read_buffer)
        return self.hashes


