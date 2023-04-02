import re
from typing import Optional

from pydantic import SecretStr

WHITE_SPACE_PATTERN = re.compile(r'\s+')
SEP_PATTERN = re.compile(r'[,:，：]')
NUMBER_PATTERN = re.compile(r'\d')


def get_content(v) -> Optional[str]:
    """Get content from str or SecretStr"""
    if isinstance(v, str):
        return v
    elif isinstance(v, SecretStr):
        return v.get_secret_value()
    return None


def replace_sep(s: str, repl: str) -> str:
    return re.sub(SEP_PATTERN, repl, s)


def remove_all_whitespaces(s: str) -> str:
    return re.sub(WHITE_SPACE_PATTERN, '', s)


def find_first_num(s: str, default: int) -> int:
    match = re.search(r"\d+", s)
    if match:
        return int(match.group(0))
    return default
