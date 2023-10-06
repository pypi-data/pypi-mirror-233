from src.PostTestResultsToPractiTest import GetConfigValues
from src.PostTestResultsToPractiTest import GetPTTestSetId
from src.PostTestResultsToPractiTest import ClonePTTestSet
from src.PostTestResultsToPractiTest import GetPTTest
from src.PostTestResultsToPractiTest import GetPTInstance
from src.PostTestResultsToPractiTest import PostTestResults
from src.PostTestResultsToPractiTest.EnumClass import TestResultStatus

global clonedTestSetId
 
def CreateTestSetProcess():
    try:
        GetConfigValues.GetConfigValues()
        
        testSetWeWantToCreate = GetPTTestSetId.RetrieveTestSetId(GetConfigValues.PTTestsetName_New)
        
        #if the test set we want to create is not already there, then create, otherwise re-use
        if testSetWeWantToCreate is None: 
            testSetIdToCloneFrom = GetPTTestSetId.RetrieveTestSetId(GetConfigValues.PTTestsetName_ToCloneFrom)
            if testSetIdToCloneFrom is not None:
                globals()['clonedTestSetId'] = ClonePTTestSet.ClonePTTestSet(testSetIdToCloneFrom)
                return clonedTestSetId
            else:
                raise Exception ("Test_set_to_clone_from is not valid")
        else:
            globals()['clonedTestSetId'] = testSetWeWantToCreate
            
    except Exception as msg:
        print ("Something went wrong in CreateTestSetProcess(): ", msg)
        raise Exception (msg)
    
def PostToPractiTest(featureFileName, passFailStatus, testOutputMessage): 
    try:
        #get associated test id (in PT) based on 'feature name' from bdd
        testId = GetPTTest.RetrieveTestId(featureFileName)

        #get associated instance id for testId provided
        instanceId = GetPTInstance.RetrieveInstanceId(clonedTestSetId, testId)
        
        if not isinstance(passFailStatus, TestResultStatus):
            raise TypeError("passFailStatus must be an instance of enum TestResultStatus")

        #post test results
        postId = PostTestResults.PostTestResultsToPT(instanceId, passFailStatus, testOutputMessage)
        print ("Post id: ", postId)
        
    except Exception as msg:
        print ("Something went wrong in PostToPractiTest(): ", msg)
        raise Exception (msg)
    


        