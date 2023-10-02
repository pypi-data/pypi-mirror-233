import dotenv
import os
from pathlib import Path
import keyring
from datetime import datetime

class models:
    DEFAULT = "A"
    ADVANCED = "A"
    BASIC = "B"

class tier:
    NONE = "NONE"
    BASE = "BASE"
    PAID = "PAID"

APP_DOMAIN = "https://platitude.ai/"
API_DOMAIN = "https://us-central1-peregrine-ai.cloudfunctions.net/api"

# for Development
# APP_DOMAIN = "http://localhost:3000"
# API_DOMAIN = "http://localhost:4244"

env_path = Path.home().joinpath(".platitude-ai")
env_file_path = env_path.joinpath(".env")

def envExists():
    return env_file_path.exists()

def createNewEnv():
    Path.mkdir(env_path, exist_ok=True)
    Path.touch(env_file_path, exist_ok=True)

    loadFromEnv()
    writeDefaultEnv()
    loadFromEnv()



def writeDefaultEnv():
    setModel(models.DEFAULT)              # write the default model, tier
    setTier(tier.NONE)    
    setUid("")
    
    # now = datetime.now()
    # _writeNow = now.strftime("%m/%d/%y_%H:%M:%S")
    # setTime()

    return {"TIER": tier.NONE, "MODEL": models.DEFAULT, "UID": ""}

def getEnv():
    model = getModel()
    tier = getTier()
    uid = getUid()

    return {"TIER": tier, "MODEL": model, "UID": uid}

def loadFromEnv():
    dotenv.load_dotenv(dotenv_path=env_file_path)

def removeLocalUser():
    clearUserTokens()
    writeDefaultEnv() 

def getModel():
    model = os.getenv("MODEL")
    return model
 
def setModel(model: str):
    dotenv.set_key(env_file_path, "MODEL", model)


def getUid():
    uid = os.getenv("UID")
    return uid
 
def setUid(uid: str):
    dotenv.set_key(env_file_path, "UID", uid)


def getTier():
    tier = os.getenv("TIER")
    return tier

def setTier(new_tier: str):
    dotenv.set_key(env_file_path, "TIER", new_tier)

def saveUserTokens(email, id_token, refresh_token):
    try:
        keyring.set_password("Platitude-AI", "email", email)
        keyring.set_password("Platitude-AI", "idToken", id_token)
        keyring.set_password("Platitude-AI", "refreshToken", refresh_token)
    except Exception as e:
        return False

    return True

def loadUserTokens():
    try:
        id_token = keyring.get_password("Platitude-AI", "idToken")
        refresh_token = keyring.get_password("Platitude-AI", "refreshToken")
    except Exception as e:
        return (None, None)
    
    return (id_token, refresh_token)

def loadUserEmail():
    try:
        email = keyring.get_password("Platitude-AI", "email")
    except Exception as e:
        return None
    
    return email
    

def clearUserTokens():
    try:
        keyring.delete_password("Platitude-AI", "idToken")
        keyring.delete_password("Platitude-AI", "refreshToken")
        keyring.delete_password("Platitude-AI", "email")
    except Exception as e:
        pass


def userTokensExist():

    try: 
        id_token = keyring.get_password("Platitude-AI", "idToken")
    except:
        return False
    
    if id_token and type (id_token) == str:
        return True
    
    return False
