#!/usr/bin/env python3
""" SESSION AUTH module
"""
import base64
from typing import TypeVar
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session class for handling session authentication
    """

    user_id_by_session_id = {}

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a SessionAuth instance
        """
        super().__init__(*args, **kwargs)
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user_id

        Path parameter:
        - user_id (str): The ID of the User.
        Return:
            - Session ID
            - None if user_id is none or not a string
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
