#!/usr/bin/env python3
""" SESSION AUTH EXPIRY module
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """Session expiration-based authentication class."""
    
    def __init__(self):
        """Override __init__ to set session_duration from environment variable."""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0
    
    def create_session(self, user_id=None):
        """Override create_session to include session expiration."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        
        self.user_id_by_session_id[session_id] = session_dict
        return session_id
    
    def user_id_for_session_id(self, session_id=None):
        """Override user_id_for_session_id to consider session expiration."""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        
        session_dict = self.user_id_by_session_id[session_id]
        
        if self.session_duration <= 0:
            return session_dict["user_id"]
        
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        
        return session_dict["user_id"]
