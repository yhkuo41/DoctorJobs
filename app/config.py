import os
from typing import Optional

from dotenv import load_dotenv

if not load_dotenv():
    load_dotenv(dotenv_path="/usr/doctorjobs/.env")


def get_secret(name: str, default: str = None) -> Optional[str]:
    return os.environ.get(name, default)
