#!/usr/bin/env python3
""" SESSION AUTH module
"""
import base64
from os import getenv
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user ID based on Session ID

        Path parameter:
        - session_id (str): The ID of the session.
        Return:
            - user ID
            - None if session_id is none or not a string
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
    
    def current_user(self, request=None):
        """ Returns user isntance based on cookie value

        Path parameter:
        - request (str): The request containing the cookie
        Return:
            - user instance
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)
