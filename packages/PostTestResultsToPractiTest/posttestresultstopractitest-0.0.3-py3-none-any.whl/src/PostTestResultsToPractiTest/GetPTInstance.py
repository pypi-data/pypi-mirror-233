import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import GetPTProjectId
from src.PostTestResultsToPractiTest import Constants

def RetrieveInstanceId(filterByTestSetId, filterByTestId):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    
    res = PT_APIRequest.getRequest(Constants.PT_API_BASEURL+ "/projects/" + projectId + "/instances.json?set-ids=" + filterByTestSetId)

    if res.status_code == 200:
        allInstances = json.loads(res.content)
        allInstancesData = allInstances['data']
        myInstanceData = list(filter(lambda myData:myData['attributes']['test-id']==int(filterByTestId), allInstancesData))   
        #print ("testData:", myInstanceData)
               
        if len(myInstanceData) != 0:
            myInstanceId = myInstanceData[0]['id']
            print ("Instance id:", myInstanceId)
            return myInstanceId
        else:
            raise Exception ("No associated instance is found in PT that has the key of 'test-id'= " + filterByTestId)
    else:
        raise Exception ("Call to get a list of instances is unsucessful with status code", res.status_code)
