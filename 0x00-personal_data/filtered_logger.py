#!/usr/bin/env python3

"""

This module contains the function, which is used
to obfuscate specified fields

"""

import logging
import re
from typing import List
import os
import mysql.connector
import mysql.connector.connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (list[str]): List of field names.
        redaction (str): The string to replace the field values with.
        message (str): The original log line to process.
        separator (str): The character separating each field in the log line.

    Returns:
        str: The obfuscated log message with sensitive fields.
    """
    msg = re.sub(rf'({"|".join(fields)})=.*?{separator}', lambda
                 m: f'{m.group(1)}={redaction}{separator}', message)
    return msg


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named 'user_data'
    with specific settings.

    Returns:
        logging.Logger: Configured logger object
        with RedactingFormatter.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)

def get_db()-> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to a MySQL database """
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", 'root')
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", '')
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", 'localhost')
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connection.MySQLConnection(user=db_user, password=db_pwd,
                              host=db_host, database=db_name)
    return connection
