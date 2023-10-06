import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import GetPTProjectId
from src.PostTestResultsToPractiTest import Constants

def RetrieveTestId(filterByAutomationName):
    GetConfigValues.GetConfigValues()
    projectId = GetPTProjectId.RetrieveProjectId()
    res = PT_APIRequest.getRequest(Constants.PT_API_BASEURL + "/projects/" + projectId + "/tests.json")
    
    if res.status_code == 200:
        allTests = json.loads(res.content)
        allTestsData = allTests['data']

        myTestData = list(filter(lambda myData: myData.get('attributes').get('custom-fields').get('---f-114228') == filterByAutomationName, allTestsData ))
       
        if len(myTestData) != 0:
            myTestId = myTestData[0]['id']
            print ("Test id:", myTestId)
            return myTestId
        else:
            raise Exception ("No associated test is found in PT that has the key of 'Automation Name = '" + filterByAutomationName)
    else:
        raise Exception ("Call to get a list of tests is unsucessful with status code", res.status_code)

#retrieveProjectId()