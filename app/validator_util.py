from typing import Optional

from pydantic import SecretStr


def get_content(v) -> Optional[str]:
    """Get content from str or SecretStr"""
    if isinstance(v, str):
        return v
    elif isinstance(v, SecretStr):
        return v.get_secret_value()
    return None
