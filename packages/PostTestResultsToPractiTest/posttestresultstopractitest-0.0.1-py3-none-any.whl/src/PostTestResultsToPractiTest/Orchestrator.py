import json
import PT_APIRequest
import GetConfigValues
import GetPTTestSetId
import GetPTProjectId
import ClonePTTestSet

def CreateTestSetProcess():
    try:
        GetConfigValues.GetConfigValues()
        testSetIdToCloneFrom = GetPTTestSetId.RetrieveTestSetId()
        
        clonedTestSetId = ClonePTTestSet.ClonePTTestSet(testSetIdToCloneFrom)
        
    except Exception as msg:
        print ("Something went wrong: ", msg)
        raise Exception (msg)
    

CreateTestSetProcess()
        