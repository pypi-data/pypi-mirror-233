import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import GetPTProjectId
from src.PostTestResultsToPractiTest import Constants

def RetrieveTestSetId(testSetName):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    
    res = PT_APIRequest.getRequest(Constants.PT_API_BASEURL + "/projects/" + projectId + "/sets.json?name_exact=" + testSetName)

    if res.status_code == 200:
        testSets = json.loads(res.content)
        testSet = testSets['data']

        myTestSetData = list(filter(lambda myData:myData['attributes']['name']==testSetName, testSet)) 
        
        if len(myTestSetData) != 0:
            myTestSetId = myTestSetData[0]['id']
            print (testSetName, "--> Test set id:", myTestSetId)
            return myTestSetId
        else:
            print ("No matching test set of " + testSetName + " is found")
            return None
    else:
        raise Exception ("Call to get test set was unsucessful with status code", res.status_code)
