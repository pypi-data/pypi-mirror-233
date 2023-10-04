import json
from src.PostTestResultsToPractiTest import PT_APIRequest
from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import GetPTTestSetId
from src.PostTestResultsToPractiTest import GetPTProjectId
from src.PostTestResultsToPractiTest import ClonePTTestSet

def CreateTestSetProcess():
    try:
        GetConfigValues.GetConfigValues()
        testSetIdToCloneFrom = GetPTTestSetId.RetrieveTestSetId()
        
        clonedTestSetId = ClonePTTestSet.ClonePTTestSet(testSetIdToCloneFrom)
        
    except Exception as msg:
        print ("Something went wrong: ", msg)
        raise Exception (msg)
    

CreateTestSetProcess()
        