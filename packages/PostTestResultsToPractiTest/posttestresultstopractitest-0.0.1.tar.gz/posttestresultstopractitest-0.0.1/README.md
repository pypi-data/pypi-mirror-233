# PostTestResultsToPractiTest package

Use this package to post test results to PractiTest.
Need to create the a file called userInputs.ini at the root and add the following lines to the content of that file 

    [UserInputs]
    PractiTestProjectName=<PTprojectName>
    PractiTestTestSetName_ToCloneFrom=<TestSetNameToCloneFrom>
    PractiTestTestSetName_New=<NewTestSetName>
    PT_API_BaseURL=https://api.practitest.com/api/v2
    PT_Token=<yourPractiTestToken>