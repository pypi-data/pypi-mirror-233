import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import Constants

def RetrieveProjectId():
    GetConfigValues.GetConfigValues()
    res = PT_APIRequest.getRequest(Constants.PT_API_BASEURL + "/projects.json")

    if res.status_code == 200:
        projects = json.loads(res.content)
        project = projects['data']
        myProjectData = list(filter(lambda myData:myData['attributes']['name']==GetConfigValues.PTProjectName, project)) 
        
        if len(myProjectData) != 0:
            myProjectId = myProjectData[0]['id']
            return myProjectId
        else:   
            raise Exception("No matching project id of " + GetConfigValues.PTProjectName + " is found")          
    else:
        raise Exception("Call to get project id was unsucessful with status code", res.status_code)