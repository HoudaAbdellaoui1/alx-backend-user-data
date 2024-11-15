#!/usr/bin/env python3
""" AUTH module
"""
from typing import List, TypeVar
from flask import request
from models import user


class Auth():
    """ Auth class for handling authentication
    """
    
    @classmethod
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a path requires authentication.
        """
        return False

    @classmethod
    def authorization_header(self, request=None) -> str:
        """Retrieves the Authorization header from the request
        """
        return None
    
    @classmethod
    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user
        """
        return None
