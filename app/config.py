import os
from typing import Optional

from dotenv import load_dotenv
from get_docker_secret import get_docker_secret

has_env_file = load_dotenv()
env_dict = {}


def get_secret(name: str) -> Optional[str]:
    if has_env_file:  # local dev
        return os.environ.get(name)
    if not env_dict:  # docker
        for line in get_docker_secret("doctorjobs_env").splitlines():
            line = line.strip()
            kv = line.split("=", 1)
            if len(kv) == 2:
                env_dict[kv[0].strip()] = kv[1].strip().strip("'").strip('"')
    return env_dict.get(name)
