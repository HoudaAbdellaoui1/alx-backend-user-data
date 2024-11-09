#!/usr/bin/env python3

# This module contains the function, which is used
# to obfuscate specified fields
import re


def filter_datum(fields: list[str], redaction: str, message: str,
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
    return re.sub(rf'({"|".join(fields)})=.*?{separator}',
                  lambda m: f'{m.group(1)}={redaction}{separator}', message)
