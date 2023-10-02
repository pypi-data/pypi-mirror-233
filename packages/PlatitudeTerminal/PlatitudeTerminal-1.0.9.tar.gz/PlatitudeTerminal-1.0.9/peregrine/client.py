import json
from peregrine import stateutils
import requests

class KeyNotFoundError(Exception):
    pass

def check_env(func):
    def wrapper(*args, **kwargs):
    
        retval = func(*args, **kwargs)
        return retval
        
    return wrapper

@check_env
def suggest(user_text: str, idToken: str, uid: str) -> str:
    
    model = stateutils.getModel()
    url = stateutils.API_DOMAIN + "/query"
    headers = {'Authorization': f'Bearer {idToken}', 'Content-Type': 'application/json'}
    body = {
        'model': model,
        'query_type': 'suggest',
        'user_text': user_text,
        'uid': uid
    }

    _response = requests.post(url, headers=headers, data=json.dumps(body))
    _response.raise_for_status()
    response = _response.json()
    response_cmd = response['response']
    usage = response['usage']
    
    return (response_cmd, usage)

@check_env
def explain(user_text: str, idToken: str, uid: str) -> str:
    
    model = stateutils.getModel()
    url = stateutils.API_DOMAIN + "/query"
    headers = {'Authorization': f'Bearer {idToken}', 'Content-Type': 'application/json'}
    body = {
        'model': model,
        'query_type': 'explain',
        'user_text': user_text,
        'uid': uid
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    response.raise_for_status()
    response_json = response.json()
    response_cmd = response_json['response']
    usage = response_json['usage']
    
    return (response_cmd, usage)


def chat(user_text: str, idToken: str, uid: str) -> str:
    
    model = stateutils.getModel()
    url = stateutils.API_DOMAIN + "/query"

    headers = {'Authorization': f'Bearer {idToken}', 'Content-Type': 'application/json'}
    body = {
        'model': model,
        'query_type': 'chat',
        'user_text': user_text,
        'uid': uid
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    response.raise_for_status()
    response_json = response.json()
    response_cmd = response_json['response']
    usage = response_json['usage']
    
    return (response_cmd, usage)

@check_env
def alternatives(user_text: str, idToken: str, uid: str) -> str:

    model = stateutils.getModel()
    url = stateutils.API_DOMAIN + "/query"
    headers = {'Authorization': f'Bearer {idToken}', 'Content-Type': 'application/json'}
    body = {
        'model': model,
        'query_type': 'alt',
        'user_text': user_text,
        'uid': uid
    }

    _response = requests.post(url, headers=headers, data=json.dumps(body))
    _response.raise_for_status()
    response = _response.json()
    response_cmd = response['response']
    usage = response['usage']

    return (response_cmd, usage)


    