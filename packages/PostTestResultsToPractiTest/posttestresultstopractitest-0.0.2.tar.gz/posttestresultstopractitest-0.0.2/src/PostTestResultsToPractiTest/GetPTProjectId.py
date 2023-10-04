import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues

def RetrieveProjectId():
    GetConfigValues.GetConfigValues()
    res = PT_APIRequest.getRequest(GetConfigValues.PT_API_BaseURL + "/projects.json")

    #print (res.status_code)
    #print (res.text)
    #print (res.content)
    if res.status_code == 200:
        projects = json.loads(res.content)
        print(type(projects))

        project = projects['data']

        myProjectData = list(filter(lambda myData:myData['attributes']['name']==GetConfigValues.PTProjectName, project)) 
        if len(myProjectData) != 0:
            myProjectId = myProjectData[0]['id']
            print (myProjectId)
            return myProjectId
        else:   
            raise Exception("No matching project id of " + GetConfigValues.PTProjectName + "is found")          
    else:
        raise Exception("Call to get project id was unsucessful with status code", res.status_code)