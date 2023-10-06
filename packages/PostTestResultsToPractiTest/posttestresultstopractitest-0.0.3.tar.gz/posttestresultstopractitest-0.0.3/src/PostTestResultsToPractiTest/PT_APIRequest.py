import requests
from src.PostTestResultsToPractiTest import GetConfigValues

def getRequest(url):
    res = requests.get(url, auth=('',GetConfigValues.PT_Token))
    return res

def sendRequest(url, putOrPostMethod, jsonData):
    if putOrPostMethod.lower() == "put":
        res = requests.put(url, data=jsonData, auth=('',GetConfigValues.PT_Token), headers={'Content-type': 'application/json'})
        
    elif putOrPostMethod.lower() == "post":
        res = requests.post(url, data=jsonData, auth=('',GetConfigValues.PT_Token), headers={'Content-type': 'application/json'})
    
    return res