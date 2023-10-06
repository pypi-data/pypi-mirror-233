# PostTestResultsToPractiTest package

## Config file requirements: 
    Need to create a file called userInputs.ini at the root of your project and add the following lines to the content of that file.  You'll need to update those values with your specific ones. 
    
        ```
        [UserInputs]
        PractiTestProjectName=<PractiTest's Project Name>
        PractiTestTestSetName_ToCloneFrom=<TestSetNameToCloneFrom>
        PractiTestTestSetName_New=<NewTestSetNameToBeCreated>
        PT_Token=<yourPractiTestToken>
        ```


## This package makes use of PractiTest's APIs to do the following:

### 1. Use this package to create test_set (to be used in step 2)

    Example of how to use it (in Python):
    ```
        from src.PostTestResultsToPractiTest import Orchestrator
        Orchestrator.CreateTestSetProcess()
    ```

### 2. Use this package to post test results to the test_set created in step1.

    Example of how to use it (in Python):
    ```
        from src.PostTestResultsToPractiTest import Orchestrator
        from src.PostTestResultsToPractiTest.EnumClass import TestResultStatus
        Orchestrator.PostToPractiTest("NameOfYourFeatureFileInBDD-including-extension-.feature", TestResultStatus.UNSTABLE, "Output message if any")
    ```
    Note that TestResultStatus is an enum class, available values are TestResultStatus.PASS, estResultStatus.FAIL, and TestResultStatus.UNSTABLE