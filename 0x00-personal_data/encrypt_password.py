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
