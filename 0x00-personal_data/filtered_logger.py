#!/usr/bin/env python3
import logging
import re
logger = logging.getLogger(__name__)


def filter_datum(fields, redaction, message, separator):
    return re.sub(rf'({"|".join(fields)})=.*?{separator}',
                  lambda m: f'{m.group(1)}={redaction}{separator}', message)
