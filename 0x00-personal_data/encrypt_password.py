#!/usr/bin/env python3

"""

This module contains the functions used to
encrypt user passwords

"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    encrypts a password using bcrypt

    Args:
        password (str): password to encrypt.

    Returns:
        bytes: The encrypted pwd.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    check if password is valid

    Args:
        hashed_password (bytes): hashed version
        password (str): original version

    Returns:
        bool: True / False
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
