import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import GetPTProjectId
from src.PostTestResultsToPractiTest import Constants

def ClonePTTestSet(testSetIdTocloneFrom):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    
    jsonData = json.dumps({"data":{"type":"sets","attributes":{"name":GetConfigValues.PTTestsetName_New,"priority":"highest"}}})
    
    res = PT_APIRequest.sendRequest(Constants.PT_API_BASEURL + "/projects/" + projectId +"/sets/" + testSetIdTocloneFrom + "/clone.json", "post", jsonData)
    #print (res.status_code)
    #print (res.text)
    #print (res.content)
    if res.status_code == 200:
        responseData = json.loads(res.content)
        #print(type(testSets))

        data = responseData['data']
   
        newTestSetId = data['id']
        print ("TestSetName:", GetConfigValues.PTTestsetName_New, "-->New test set id: " + newTestSetId)
        return newTestSetId
    else:
        raise Exception ("Call to clone test set was unsucessful with status code", res.status_code)
