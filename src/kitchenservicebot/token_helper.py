import json
import sys
from pathlib import Path


def get_token() -> int:
    """Get token for discord bot in json file."""
    try:
        with Path("token.json").open() as json_file:
            token = json.load(json_file).get("token")
            if not token:
                sys.exit('Invalid token.json syntax -> {"token": token}')
            json_file.close()
    except FileNotFoundError:
        sys.exit('Add json file with following syntax: token.json -> {"token": token}')

    return token
