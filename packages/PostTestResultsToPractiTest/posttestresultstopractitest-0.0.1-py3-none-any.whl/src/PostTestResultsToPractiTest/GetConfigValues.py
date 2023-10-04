import configparser
import os

def GetConfigValues(): 
    global PTProjectName 
    global PTTestsetName_ToCloneFrom
    global PT_Token
    global PT_API_BaseURL
    global PTTestsetName_New
    
    userInputs = configparser.ConfigParser()
    iniPath = os.path.join(os.getcwd(), '../../userInputs.ini')
    userInputs.read(iniPath)    
    
    PTProjectName = userInputs['UserInputs']['PractiTestProjectName']
    print ("ptPRojectname:", PTProjectName)

    PTTestsetName_ToCloneFrom = userInputs['UserInputs']['PractiTestTestSetName_ToCloneFrom']
    print ("PT test set name to clone from:", PTTestsetName_ToCloneFrom)

    PT_Token = userInputs['UserInputs']['PT_Token']
    
    PT_API_BaseURL = userInputs['UserInputs']['PT_API_BaseURL']
    print ("PT base URL:", PT_API_BaseURL)
    
    PTTestsetName_New = userInputs['UserInputs']['PractiTestTestSetName_New']
    print ("PT test set name (new):", PTTestsetName_New)
    
    