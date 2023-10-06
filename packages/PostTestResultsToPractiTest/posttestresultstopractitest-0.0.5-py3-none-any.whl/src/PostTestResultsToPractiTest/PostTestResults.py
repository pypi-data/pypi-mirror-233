import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import GetPTProjectId
from src.PostTestResultsToPractiTest import Constants
from src.PostTestResultsToPractiTest.EnumClass import TestResultStatus

def PostTestResultsToPT(instanceId, passFailStatus, testOutputMessage):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
  
    print ("passfailStatus..", passFailStatus)  
    if passFailStatus.value == "pass":
        exit_code = 0
    else:
        exit_code = 1
        
    jsonData = json.dumps({"data":{"type":"instances","attributes":{"instance-id":instanceId,"exit-code":exit_code,"automated-execution-output":testOutputMessage}}})
    
    res = PT_APIRequest.sendRequest(Constants.PT_API_BASEURL + "/projects/" + projectId + "/runs.json", "post", jsonData)
    
    if res.status_code == 200:
        responseData = json.loads(res.content)
        data = responseData['data']
        postId = data['id']
        return postId
    else:
        raise Exception ("Call to post-results-to-PT was unsucessful with status code", res.status_code)
