import asyncio, threading, mystring as mys
from typing import List, Dict, Union
from datetime import datetime
from ephfile import ephfile
from pnostic.structure import RepoObject, RepoResultObject, RepoObjectProvider, Runner, LoggerSet, Logger
import type_enforced

waiting = lambda:True

runnerList:List[str] = []
runnerListLock = threading.Lock()

fileList:List[str] = []
fileListLock = threading.Lock()

async def perRunnerSingleRun(repoFiles: RepoObjectProvider, runners:List[Runner], loggersset:List[Logger]):
    loggers:LoggerSet = LoggerSet()
    [loggers.add(x) for x in loggersset]

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

                        firstScanResults = await perFile(fileObj, runner, loggersset)
                        runnerLog("Got the 1st results from file {0}".format(fileObj.filename))
                        runnerLog(firstScanResults)

                        vulnRepoResults:List[RepoResultObject] = [x for x in firstScanResults if x.IsVuln]
                        runnerLog("Has a vulnerability? : {0}".format(len(vulnRepoResults) > 0))

                        runnerLog("Running the waiter")
                        waiting()

                    with mys.session(fileListLock):
                        fileList += [fileObj.filename]

            with mys.session(runnerListLock):
                runnerList += [runner.name]

async def perRunnerDoubleRunCorrect(repoFiles: RepoObjectProvider, runners:List[Runner], loggersset:List[Logger]):
    loggers:LoggerSet = LoggerSet()
    [loggers.add(x) for x in loggersset]

    for runnerSvr in runners:
        runnerSvr.initialize()
        runnerLog("Initialized Runner")
        with loggers.__enter__("Runner {0}".format(runner.name)) as runnerLog:
            for fileObj in repoFiles.files:
                with mys.session(fileListLock):
                    fileList = []

                runnerLog(fileObj)
                with loggers.__enter__("File {0}".format(fileObj.filename)):
                    firstScanResults: List[RepoResultObject] = None

                    firstScanResults = await perFile(fileObj, runner, loggersset)
                    runnerLog("Got the 1st results from file {0}".format(fileObj.filename))
                    runnerLog(firstScanResults)

                    vulnRepoResults:List[RepoResultObject] = [x for x in firstScanResults if x.IsVuln]
                    runnerLog("Has a vulnerability? : {0}".format(len(vulnRepoResults) > 0))

                    if len(vulnRepoResults) > 0:
                        secondScanResults: List[RepoResultObject] = None

                        fileObj.content = vulnRepoResults[0].correctedCode
                        secondScanResults = await perFile(fileObj, runner, loggersset)
                        runnerLog(secondScanResults)
                        runnerLog("Got the 2nd results from file {0}".format(fileObj.filename))

                        vulnRepoResultsTwo:List[RepoResultObject] = [x for x in secondScanResults if x.IsVuln]
                        runnerLog("Has a vulnerability? : {0}".format(len(vulnRepoResultsTwo) > 0))

                    runnerLog("Running the waiter")
                    waiting()

                with mys.session(fileListLock):
                    fileList += [fileObj.filename]

        runnerSvr.clean()
        with mys.session(runnerListLock):
            runnerList += [runner.name]


async def perFile(fileObj:RepoObject, runner:Runner, loggersset:List[Logger])-> List[RepoResultObject]:
    loggers:LoggerSet = LoggerSet()
    [loggers.add(x) for x in loggersset]

    output:List[RepoResultObject] = []
    with loggers.__enter__("Scanning {0} with {1}".format(fileObj.filename, runner.name)) as scannerLog:
        with ephfile("{0}_stub.py".format(runner.name), fileObj.content) as eph:
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