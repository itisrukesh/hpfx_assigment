import os
from enum import Enum
from dotenv import load_dotenv

CREDSFILE = 'credentials.json'
TOKENFILE = 'token.json'

# From this we are getting how many number of mail we should fetch, 
# we will also use this for batch storing as well.
BATCHCOUNT = 50

class ConfigVars(Enum):
    PORT = "PORTVAL"
    SCOPESSTRINGS = "SCOPESVAL"
    DBFILE = "DBFILEVAL"
    TABLE = "TABLEVAL"

# Loads values from .env / os env
load_dotenv(override=True)

#Get PORT
PORT = int(os.getenv(ConfigVars.PORT.value))
if PORT:
    print(PORT)
else: print(f"{ConfigVars.PORT.value} environment variable not found.")

# Get DBFile value:
DBFILE = os.getenv(ConfigVars.DBFILE.value)
if DBFILE:
    print(DBFILE)
else: print(f"{ConfigVars.DBFILE.value} environment variable not found.")

# Get TableName value:
TABLE = os.getenv(ConfigVars.TABLE.value)
if TABLE:
    print(TABLE)
else: print(f"{ConfigVars.TABLE.value} environment variable not found.")

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