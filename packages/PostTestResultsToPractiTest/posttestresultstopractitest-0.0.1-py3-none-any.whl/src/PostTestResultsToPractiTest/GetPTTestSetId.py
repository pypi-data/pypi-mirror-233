import json
import PT_APIRequest
import GetConfigValues
import GetPTProjectId

def RetrieveTestSetId():
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    
    res = PT_APIRequest.getRequest(GetConfigValues.PT_API_BaseURL + "/projects/" + projectId + "/sets.json?name_exact=" + GetConfigValues.PTTestsetName_ToCloneFrom)

    #print (res.status_code)
    #print (res.text)
    #print (res.content)
    if res.status_code == 200:
        testSets = json.loads(res.content)
        #print(type(testSets))

        testSet = testSets['data']

        myTestSetData = list(filter(lambda myData:myData['attributes']['name']==GetConfigValues.PTTestsetName_ToCloneFrom, testSet)) 
        
        if len(myTestSetData) != 0:
            myTestSetId = myTestSetData[0]['id']
            print (myTestSetId)
            return myTestSetId
        else:
            raise Exception ("No matching test set of " + GetConfigValues.PTTestsetName_ToCloneFrom + "is found")
    else:
        raise Exception ("Call to get test set was unsucessful with status code", res.status_code)

#retrieveProjectId()