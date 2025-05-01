import os
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path
from typing import List
from logger import app_logger as log

# Load .env values
load_dotenv(override=True)

class ConfigVars(Enum):
    PORT = "PORTVAL"
    SCOPESSTRINGS = "SCOPESVAL"
    DBFILE = "DBFILEVAL"
    EMAILSTABLE = "EMAILSTABLEVAL"
    HISTORYTABLE = "HISTORYTABLEVAL"
    # json files
    CREDSFILE = "CREDSFILE"
    DEFAULT_CREDSFILE = "credentials.json"
    TOKENFILE = "TOKENFILE"
    DEFAULT_TOKENFILE = "token.json"
    #Additional Vars used in codebase:
    BATCHCOUNT = "BATCHCOUNT"
    BATCHVALUE = 50


def _required(key: str) -> str:
    value = os.getenv(key)
    if not value:
        log.error(f"Missing required environment variable: {key}")
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value


def _required_int(key: str) -> int:
    val = _required(key)
    try:
        return int(val)
    except ValueError:
        log.error(f"{key} must be an integer")
        raise ValueError(f"{key} must be an integer")


def _parse_list(key: str) -> List[str]:
    val = os.getenv(key, "")
    if val == '':
        log.error(f'SCOPES are empty-string')
        raise ValueError(f'SCOPES are empty-string')
    return [s.strip() for s in val.split(",") if s.strip()]


CREDSFILE: str = os.getenv(ConfigVars.CREDSFILE.value, ConfigVars.DEFAULT_CREDSFILE.value)
TOKENFILE: str = os.getenv(ConfigVars.TOKENFILE.value, ConfigVars.DEFAULT_TOKENFILE.value)
BATCHCOUNT: int = int(os.getenv(ConfigVars.BATCHCOUNT.value, ConfigVars.BATCHVALUE.value))

PORT: int = _required_int(ConfigVars.PORT.value)
SCOPES: List[str] = _parse_list(ConfigVars.SCOPESSTRINGS.value)
DBFILE: str = _required(ConfigVars.DBFILE.value)
EMAILSTABLE: str = _required(ConfigVars.EMAILSTABLE.value)
HISTORYTABLE: str = _required(ConfigVars.HISTORYTABLE.value)
log.info("Config variable Loaded!")