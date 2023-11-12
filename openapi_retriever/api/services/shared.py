"""Define shared functions for the API."""
import hashlib
import os
from typing import Optional


class Cache:

    @staticmethod
    def hash(value: str) -> str:
        """
        Generate an MD5 hash of a string.
        
        Args:
            value: The string to hash.
            
        Returns:
            The MD5 hash of the string.
        """
        hash_obj = hashlib.md5()
        hash_obj.update(value.encode('utf-8'))
        return hash_obj.hexdigest()

    @staticmethod
    def get(value: str) -> Optional[str]:
        """
        Retrieve a cached string from a local file cache.
        
        Args:
            hash_hex: The MD5 hash of the string to retrieve.
            
        Returns:
            The cached string if it exists, or an empty string if it does not.
        """
        hash_hex = Cache.hash(value)
        filename = os.path.join('/tmp', hash_hex)
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    @staticmethod
    def set(value: str) -> str:
        """
        Cache a string in a local file cache.
        
        Args:
            input_string: The string to cache.
            
        Returns:
            The MD5 hash of the cached string.
        """
        hash_hex = Cache.hash(value)
        filename = os.path.join('/tmp', hash_hex)
        
        with open(filename, 'w') as f:
            f.write(value)
        return hash_hex
