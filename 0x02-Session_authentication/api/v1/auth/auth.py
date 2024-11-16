#!/usr/bin/env python3
""" AUTH module
"""
import fnmatch
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
        if path is None:
            return True

        if not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    @classmethod
    def authorization_header(self, request=None) -> str:
        """Retrieves the Authorization header from the request
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    @classmethod
    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user
        """
        return None
