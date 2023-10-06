from src.PostTestResultsToPractiTest import Orchestrator
from src.PostTestResultsToPractiTest.EnumClass import TestResultStatus

def main():
    Orchestrator.CreateTestSetProcess()
    Orchestrator.PostToPractiTest("AKDayInLifeTestsTS.feature", TestResultStatus.UNSTABLE, "Output message if any")
    
main()