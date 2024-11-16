#!/usr/bin/env python3
""" BASIC AUTH module
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class for handling basic authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the header, or None if invalid.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Extracts and decodes the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The decoded UTF-8 string from the Base64 part,
            or None if invalid.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header,
                                             validate=True)
            decoded_string = decoded_bytes.decode('utf-8')
        except Exception:
            return None

        return decoded_string

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts the user email and password from the decoded
        Base64 string of the Authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded
            Base64 part of the Authorization header.

        Returns:
            tuple: A tuple containing the user email and password,
            or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(":", 1)

        return email, password

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on their email and password """

        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        if User.all() is None:
            return

        results = User.search({'email': user_email})
        if not results:
            return None

        if not results[0].is_valid_password(user_pwd):
            return None

        return results[0]

    def current_user(self, request=None) -> TypeVar('User'):
        authorization_header = self.authorization_header(request)
        if not authorization_header:
            return None

        header = self.extract_base64_authorization_header(authorization_header)
        if not header:
            return None

        decoded = self.decode_base64_authorization_header(header)
        if not decoded:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded)
        if not user_email or not user_pwd:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
