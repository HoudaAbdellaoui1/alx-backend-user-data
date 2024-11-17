#!/usr/bin/env python3
""" SESSION DB AUTH module
"""
from datetime import datetime, timedelta
from os import getenv
from typing import TypeVar
import uuid

from flask.json import jsonify
from flask import request
from api.v1.auth.auth import Auth
from models.user import User
from api.v1.views import app_views
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session class for handling session authentication
    """

    user_id_by_session_id = {}

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a SessionAuth instance
        """
        super().__init__(*args, **kwargs)
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a new instance of user session and
        return the session ID

        Path parameter:
        - user_id (str): The ID of the User.
        Return:
            - Session ID
            - None if user_id is none or not a string
        """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user ID based on Session ID

        Path parameter:
        - session_id (str): The ID of the session.
        Return:
            - user ID
            - None if session_id is none or not a string
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """ Destroy an authenticated session """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
