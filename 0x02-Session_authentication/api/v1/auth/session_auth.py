#!/usr/bin/env python3
""" SESSION AUTH module
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session class for handling session authentication
    """
