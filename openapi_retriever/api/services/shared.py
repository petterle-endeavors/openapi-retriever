"""Define shared functions for the API."""
import hashlib
import os
from typing import Optional


class Cache:

    @staticmethod
    def get(key: str) -> Optional[str]:
        """
        Retrieve a cached string from a local file cache.
        
        Args:
            hash_hex: The MD5 hash of the string to retrieve.
            
        Returns:
            The cached string if it exists, or an empty string if it does not.
        """
        filename = os.path.join('/tmp', key)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        Cache a string in a local file cache.
        
        Args:
            input_string: The string to cache.
            
        Returns:
            The MD5 hash of the cached string.
        """
        filename = os.path.join('/tmp', key)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(value)
