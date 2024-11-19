"""DB module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password
    """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)
