import configparser
import os

def GetConfigValues(): 
    global PTProjectName 
    global PTTestsetName_ToCloneFrom
    global PT_Token
    global PT_API_BaseURL
    global PTTestsetName_New
        
    userInputs = configparser.ConfigParser()
    iniPath = os.path.join(os.getcwd(), 'userInputs.ini')
    userInputs.read(iniPath)    
        
    PTProjectName = userInputs['UserInputs']['PractiTestProjectName']

    PTTestsetName_ToCloneFrom = userInputs['UserInputs']['PractiTestTestSetName_ToCloneFrom']

    PT_Token = userInputs['UserInputs']['PT_Token']
        
    PTTestsetName_New = userInputs['UserInputs']['PractiTestTestSetName_New']
        
    