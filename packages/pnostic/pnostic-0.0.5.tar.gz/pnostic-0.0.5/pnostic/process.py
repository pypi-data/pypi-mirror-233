import asyncio, threading, mystring as mys
from typing import List, Dict, Union
from datetime import datetime
from ephfile import ephfile
from structure import RepoObject, RepoResultObject, RepoObjectProvider, Runner, LoggerSet
import type_enforced

loggers:LoggerSet = LoggerSet()
waiting = lambda:True

runnerList:List[str] = []
runnerListLock = threading.Lock()

fileList:List[str] = []
fileListLock = threading.Lock()

@type_enforced.Enforcer
async def perfiles(repoFiles: RepoObjectProvider, runners:List[Runner]):
    for runnerSvr in runners:
        with runnerSvr() as runner:
            runnerLog("Initialized Runner")
            with loggers.__enter__("Runner {0}".format(runner.name)) as runnerLog:
                for fileObj in repoFiles.files:
                    with mys.session(fileListLock):
                        fileList = []

                    runnerLog(fileObj)
                    with loggers.__enter__("File {0}".format(fileObj.filename)):
                        firstScanResults: List[RepoResultObject] = None

                        firstScanResults = await perfile(fileObj, runner)
                        runnerLog("Got the 1st results from file {0}".format(fileObj.filename))
                        runnerLog(firstScanResults)

                        vulnRepoResults:List[RepoResultObject] = [x for x in firstScanResults if x.IsVuln]
                        runnerLog("Has a vulnerability? : {0}".format(len(vulnRepoResults) > 0))

                        if len(vulnRepoResults) > 0:
                            secondScanResults: List[RepoResultObject] = None

                            fileObj.content = vulnRepoResults[0].correctedCode
                            secondScanResults = await perfile(fileObj, runner)
                            runnerLog(secondScanResults)
                            runnerLog("Got the 2nd results from file {0}".format(fileObj.filename))

                            vulnRepoResultsTwo:List[RepoResultObject] = [x for x in secondScanResults if x.IsVuln]
                            runnerLog("Has a vulnerability? : {0}".format(len(vulnRepoResultsTwo) > 0))

                        runnerLog("Running the waiter")
                        waiting()

                    with mys.session(fileListLock):
                        fileList += [fileObj.filename]

            with mys.session(runnerListLock):
                runnerList += [runner.name]

@type_enforced.Enforcer
async def perfile(fileObj:RepoObject, runner:Runner)-> List[RepoResultObject]:
    output:List[RepoResultObject] = []
    with loggers.__enter__("Scanning {0} with {1}".format(fileObj.filename, runner.name)) as scannerLog:
        with ephfile("stub.py", fileObj.content) as eph:
            scannerLog("Started Scanning File {0}".format(fileObj.filename))

            startTime:datetime.datetime = datetime.now().astimezone().isoformat()
            output = await runner.scan(eph())
            endTime:datetime.datetime = datetime.now().astimezone().isoformat()

            resultObject: RepoResultObject
            for resultObject in RepoResultObject:
                resultObject.startDateTime = startTime
                resultObject.endDateTime = endTime
                scannerLog(resultObject)

            scannerLog("Ended Scanning File {0}".format(fileObj.filename))
    return output