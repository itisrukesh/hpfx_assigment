import os
from enum import Enum
from dotenv import load_dotenv

CREDSFILE = 'credentials.json'
TOKENFILE = 'token.json'

class ConfigVars(Enum):
    PORT = "PORTVAL"
    SCOPESSTRINGS = "SCOPESVAL"

# Loads values from .env / os env
load_dotenv(override=True)

#Get PORT
PORT = int(os.getenv(ConfigVars.PORT.value))
if PORT:
    print(PORT)
else: print(f"{ConfigVars.PORT.value} environment variable not found.")

# Get list of Scopes values
# If modifying these SCOPES values in env, make sure to delete the token.pickle file. Else it will have old scope values in it.
SCOPES = []
scope_strings = os.getenv(ConfigVars.SCOPESSTRINGS.value)
if scope_strings:
    my_list = scope_strings.split(",")
    SCOPES.extend(my_list)
    print(SCOPES)
else:
    print(f"{ConfigVars.SCOPESSTRINGS.value} environment variable not found.")