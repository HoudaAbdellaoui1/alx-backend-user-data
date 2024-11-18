#!/usr/bin/env python3
"""
This module defines a `User` class representing
a table in a relational database
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    User Model

    Represents the `users` table in the database. Each instance of this class
    corresponds to a row in the `users` table.

    Attributes:
        __tablename__ (str): The name of the database table.
        id (int): The primary key of the user.
        email (str): The email of the user (required).
        hashed_password (str): The hashed password of the user (required).
        session_id (str): A session identifier for the user (optional).
        reset_token (str): A token for password reset functionality (optional).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
