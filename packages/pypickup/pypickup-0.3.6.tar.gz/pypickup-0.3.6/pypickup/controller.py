#! /usr/bin/python
from io import TextIOWrapper
import os
import re
import argparse
import shutil
from typing import Dict, List

from tqdm import tqdm

from pypickup.utils.htmlManager import HTMLManager
from pypickup.utils.networkManager import NetworkManager


class LocalPyPIController:

    """
    A class to download a desired package from the PyPI remote repository into a local one as a mirror.
    """

    _htmlManager = HTMLManager()
    _networkManager = NetworkManager()

    _baseHTMLFileName: str = "index.html"
    _packageHTMLFileName: str = "index.html"
    _remotePypiBaseDir: str = "https://pypi.org/simple/"

    _regexZIPAndTars = r"^(.*)\.(zip|tar.gz|tar.bz2|tar.xz|tar.Z|tar)$"
    _regexVersion = r"^(.*)==(\d+(?:\.\d+)*)$"
    # _regexVersion = r"^(.*)==(\d+\.\d+(?:\.\d+)?)$"

    _dryRunsTmpDir = "./.pypickup_tmp/"

    def __init__(self):
        self._packageName: str = None
        self._pypiLocalPath: str = None

        self._baseHTMLFileFullName: str = None
        self._packageHTMLFileFullName: str = None
        self._packageLocalPath: str = None

        self._printDefaultConfig: bool = None
        self._printAllFileNames: bool = None
        self._printVerbose: bool = None
        self._showRetries: bool = None

        self._onlySources: bool = None
        self._includeDevs: bool = None
        self._includeRCs: bool = None
        self._includePlatformSpecific: bool = None
        
        self._packageVersion: str = ""

        self._dryRun: bool = None

    def __del__(self):
        self._removeDir(self._dryRunsTmpDir, True)

    @property
    def packageName(self):
        return self._packageName

    @property
    def pypiLocalPath(self):
        return self._pypiLocalPath

    @property
    def baseHTMLFileFullName(self):
        return self._baseHTMLFileFullName

    @property
    def packageHTMLFileFullName(self):
        return self._packageHTMLFileFullName

    @property
    def packageLocalPath(self):
        return self._packageLocalPath

    @property
    def remotePyPIRepository(self):
        return self._remotePypiBaseDir

    @property
    def printDefaultConfig(self):
        return self._printDefaultConfig

    @property
    def printAllFileNames(self):
        return self._printAllFileNames

    @property
    def printVerbose(self):
        return self._printVerbose

    @property
    def showRetries(self):
        return self._showRetries

    @property
    def onlySources(self):
        return self._onlySources

    @property
    def includeDevs(self):
        return self._includeDevs

    @property
    def includeRCs(self):
        return self._includeRCs

    @property
    def includePlatformSpecific(self):
        return self._includePlatformSpecific

    @property
    def packageVersion(self):
        return self._packageVersion

    @property
    def dryRun(self):
        return self._dryRun

    @packageName.setter
    def packageName(self, new_PackageName: str):
        self._packageName = new_PackageName

        # Propagate changes
        if self._pypiLocalPath == None:
            self._pypiLocalPath = ""

        self.packageLocalPath = os.path.join(self._pypiLocalPath, self._packageName) + "/"
        self.packageHTMLFileFullName = os.path.join(self.packageLocalPath, self._packageHTMLFileName)

    @pypiLocalPath.setter
    def pypiLocalPath(self, new_PyPiLocalPath: str):
        self._pypiLocalPath = new_PyPiLocalPath

        self._pypiLocalPath = self._pypiLocalPath.replace("\\", "/")

        if "/" not in self._pypiLocalPath:
            self._pypiLocalPath = self.pypiLocalPath + "/"

        # Propagate changes
        self.baseHTMLFileFullName = os.path.join(self._pypiLocalPath, self._baseHTMLFileName)

        self.packageLocalPath = os.path.join(self._pypiLocalPath, self.packageName) + "/"
        self.packageHTMLFileFullName = os.path.join(self.packageLocalPath, self._packageHTMLFileName)

    @baseHTMLFileFullName.setter
    def baseHTMLFileFullName(self, new_baseHTMLFileFullName: str):
        self._baseHTMLFileFullName = new_baseHTMLFileFullName

    @packageHTMLFileFullName.setter
    def packageHTMLFileFullName(self, new_packageHTMLFileFullName: str):
        self._packageHTMLFileFullName = new_packageHTMLFileFullName

    @packageLocalPath.setter
    def packageLocalPath(self, new_packageLocalPath: str):
        self._packageLocalPath = new_packageLocalPath

    @printDefaultConfig.setter
    def printDefaultConfig(self, new_printDefaultConfig: bool):
        self._printDefaultConfig = new_printDefaultConfig

    @printAllFileNames.setter
    def printAllFileNames(self, new_printAllFileNames: bool):
        self._printAllFileNames = new_printAllFileNames

    @printVerbose.setter
    def printVerbose(self, new_printVerbose: bool):
        self._printVerbose = new_printVerbose

    @showRetries.setter
    def showRetries(self, new_showRetries: bool):
        self._showRetries = new_showRetries

    @onlySources.setter
    def onlySources(self, new_onlySources: bool):
        self._onlySources = new_onlySources

    @includeDevs.setter
    def includeDevs(self, new_includeDevs: bool):
        self._includeDevs = new_includeDevs

    @includeRCs.setter
    def includeRCs(self, new_includeRCs: bool):
        self._includeRCs = new_includeRCs

    @includePlatformSpecific.setter
    def includePlatformSpecific(self, new_includePlatformSpecific: bool):
        self._includePlatformSpecific = new_includePlatformSpecific

    @packageVersion.setter
    def packageVersion(self, new_packageVersion: bool):
        self._packageVersion = new_packageVersion

    @dryRun.setter
    def dryRun(self, new_dryRun: bool):
        self._dryRun = new_dryRun

    def _removeFile(self, fileName: str):
        if os.path.exists(fileName):
            os.remove(fileName)

    def _removeDir(self, directory: str, recursively: bool = False):
        if os.path.exists(directory):
            if recursively:
                shutil.rmtree(directory)
            else:
                os.rmdir(directory)

    def parseScriptArguments(self, args: argparse.ArgumentParser):
        """Parse the incoming arguments. A packageName and pypiLocalPath are expected. Besides, it initializes derived class attributes."""

        self.packageName = str(args.packageName).lower()
        specifiedVersion = re.match(self._regexVersion, self.packageName)
        if specifiedVersion:
            self.packageName = specifiedVersion[1]
            self.packageVersion = self.packageName + "-" + specifiedVersion[2]
        elif "=" in self.packageName:
            print("Incorrect version format.")
            exit(0)

        self.pypiLocalPath = args.pypiLocalPath

    def printDefaultConfigIfRequired(self):
        if self.printDefaultConfig:
            print("")
            print("DEFAULT CONFIGURATION VARIABLES:")
            print("\tIndex path (current): " + self.pypiLocalPath)
            print("")
            print("\tBase HTML file: " + self._baseHTMLFileName)
            print("\tPackage HTML file dir: " + self.packageHTMLFileFullName)
            print("\tPython repository : " + self._remotePypiBaseDir)
            print("")
            print("\tWheel filters settings file path: " + self._htmlManager.getWheelFiltersSettingsFilePath())
            print("\tDry runs path: " + self._dryRunsTmpDir)
            print("")
            print("\tIncluded zips and tars: " + self._regexZIPAndTars)
            print("")
            print("\tWheel filters enabled: " + str(self._htmlManager.areWheelFiltersEnabled()))
            print("\t\tUse the 'config' command to get the whole wheel filters configuration.")
            print("")

    def repositoryExists(self) -> bool:
        return os.path.exists(self.baseHTMLFileFullName)

    def packageExists(self) -> bool:
        """Returns whether the self._packageName already exists in the self._pypiLocalPath. If the local repository has not even been created previously, returns False."""

        if not os.path.exists(self.baseHTMLFileFullName):
            return False

        with open(self.baseHTMLFileFullName, "r") as baseHTMLFile:
            baseHTMLStr: str = baseHTMLFile.read()

        return self._htmlManager.existsHTMLEntry(baseHTMLStr, "a", self.packageName)

    def _writeFileFromTheStart(self, file: TextIOWrapper, textToWrite: str):
        file.seek(0)
        file.truncate(0)
        file.write(textToWrite)

    def _addPackagesToIndex(self, indexHTML: str, file: TextIOWrapper, entries: Dict[str, str]):
        updatedHTML: str = indexHTML
        for href, entryText in entries.items():
            _, updatedHTML = self._htmlManager.insertHTMLEntry(updatedHTML, "a", entryText, {"href": href})
        
        self._writeFileFromTheStart(file, updatedHTML)
        
        return updatedHTML

    def _printPackageNamesInHTML(self, packageFiles: List[str], message: str):
        print(message + " [" + str(len(packageFiles)) + "]:")
        for packageName in packageFiles:
            print(packageName)
        if len(packageFiles) == 0:
            print("-")
        print("")

    def _downloadFilesInLocalPath(self, packagesToDownload: Dict[str, str], indexHTML: str, htmlFile: TextIOWrapper, printVerbose: bool = False, showRetries: bool = False):
        updatedHTML: str = indexHTML

        actuallyDownloadedPackages: int = 0

        if len(packagesToDownload) == 0:
            print("No new packages in the remote to download.")
        else:
            print(str(len(packagesToDownload)) + " new packages available in the remote.")

            with tqdm(total=len(packagesToDownload), desc="Download", ncols=100, position=0, leave=True, colour="green") as progressBar:
                for fileName, fileLink in packagesToDownload.items():
                    ok, status, content = self._networkManager.getLink(fileLink, printVerbose=printVerbose, showRetries=showRetries)
                    if not ok:
                        print("\nUNABLE TO DOWNLOAD PACKAGE '" + fileName + "' (URL: " + fileLink + ")\n\tSTATUS: " + status + "\n")
                    else:
                        with open(self.packageLocalPath + fileName, "wb") as f:
                            f.write(content)

                        updatedHTML = self._addPackagesToIndex(updatedHTML, htmlFile, {"./" + fileName: fileName})

                        actuallyDownloadedPackages += 1

                    progressBar.update(1)

        print()
        print(str(actuallyDownloadedPackages) + "/" + str(len(packagesToDownload)) + " downloaded.")


class Add(LocalPyPIController):
    def __init__(self):
        LocalPyPIController.__init__(self)

    def parseScriptArguments(self, args: argparse.ArgumentParser):
        LocalPyPIController.parseScriptArguments(self, args)

        # 1. Set all the params we are going to use (let the ones we don't to None):
        self.printDefaultConfig = args.printDefaultConfig
        self.printAllFileNames = args.printAllFileNames
        self.printVerbose = args.printVerbose
        self.showRetries = args.showRetries

        self.onlySources = args.onlySources
        self.includeDevs = args.includeDevs
        self.includeRCs = args.includeRCs
        self.includePlatformSpecific = args.includePlatformSpecific

        self.dryRun = args.dryRun

        # 2. Use only the ones we have set:
        self._htmlManager.setFlags(self.printAllFileNames, self.onlySources, self.includeDevs, self.includeRCs, self.includePlatformSpecific, self.packageVersion)

        if (self.includeDevs or self.includeRCs) and self._htmlManager.areWheelFiltersEnabled():
            print("\tWARNING! Development releases (devX) or release candidates (RCs) flags are enabled, as well as the wheel filters, so they could be discarded anyway. This is caused because of the order of application: (1st) flags, (2nd) wheel filters.")
            print("\tPLEASE, CHECK OUT YOUR WHEEL FILTERS.")

        if self.dryRun:
            shutil.copytree(self.pypiLocalPath, self._dryRunsTmpDir)
            self.pypiLocalPath = self._dryRunsTmpDir

    def validPackageName(self) -> bool:
        """Checks whether the package link exists or not. If not, it returns False. True otherwise."""

        ok, status, _ = self._networkManager.getLink(self._remotePypiBaseDir + self.packageName)
        if not ok:
            print(status)
            return False

        return True

    def __createDirIfNeeded(self, directory: str):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    def __createFileIfNeeded(self, file: str):
        if not os.path.exists(file):
            open(file, "a").close()

    def initLocalRepo(self):
        """Initializes the local repository creating the needed directories (if not exist) and updating accordingly the base HTML."""

        self.__createDirIfNeeded(self.pypiLocalPath)
        self.__createDirIfNeeded(self.packageLocalPath)

        self.__createFileIfNeeded(self.baseHTMLFileFullName)

    def addNewPackageToIndex(self):
        """Adds the self.packageName package to the base HTML index, if not exists already."""

        baseHTMLFile = open(self.baseHTMLFileFullName, "r+")
        htmlContent: str = baseHTMLFile.read()

        if len(htmlContent) == 0:
            htmlContent = self._htmlManager.getBaseHTML()

        _, htmlUpdated = self._htmlManager.insertHTMLEntry(htmlContent, "a", self.packageName, {"href": "./" + self.packageName})

        self._writeFileFromTheStart(baseHTMLFile, htmlUpdated)

        baseHTMLFile.close()

    def getPackage(self):
        """Downloads all the files for the required package 'packageName', i.e. all the .whl, the .zip and the .tar.gz if necessary."""

        ok, status, pypiPackageHTML = self._networkManager.getLink(self._remotePypiBaseDir + self.packageName)
        if not ok:
            print(status)
        else:
            pypiPackageHTMLStr: str = pypiPackageHTML.decode("utf-8")

        if self.printAllFileNames:
            packageFiles: List[str] = list(self._htmlManager.getHRefsList(pypiPackageHTMLStr).keys())
            self._printPackageNamesInHTML(packageFiles, "\nRetrieved package files (before filtering)")

        pypiPackageHTMLStr = self._htmlManager.filterInHTML(pypiPackageHTMLStr, self._regexZIPAndTars)
        linksToDownload: Dict[str, str] = self._htmlManager.getHRefsList(pypiPackageHTMLStr)

        if self.printAllFileNames:
            self._printPackageNamesInHTML(list(linksToDownload.keys()), "\nTo-be-downloaded package files (after filtering)")

        packageBaseHTML: str = self._htmlManager.getBaseHTML()
        _, packageBaseHTML = self._htmlManager.insertHTMLEntry(packageBaseHTML, "h1", "Links for " + self.packageName, {})
        with open(self.packageHTMLFileFullName, "w") as packageHTML_file:
            packageHTML_file.write(packageBaseHTML)

            self._downloadFilesInLocalPath(linksToDownload, packageBaseHTML, packageHTML_file, printVerbose=self.printVerbose, showRetries=self.showRetries)
        
    def __checkPackagesInLocalButNotInRemote(self, remoteIndexHRefs: Dict[str, str], localIndexHRefs: Dict[str, str]) -> str:
        additionalPackagesMessage: str = ""
        for localPackageName, localPackageURL in localIndexHRefs.items():

            if not localPackageName in remoteIndexHRefs:
                if not (self.onlySources and os.path.splitext(localPackageName)[1] == ".whl"):
                    if additionalPackagesMessage == "":
                        additionalPackagesMessage += "Packages in the local but not in the remote (check filter settings):\n"
                    additionalPackagesMessage += localPackageName + "\n"

        return additionalPackagesMessage

    def __getNewPackagesInRemote(self, remoteIndexHRefs: Dict[str, str], localIndexHRefs: Dict[str, str]) -> Dict[str, str]:
        resultingDict: Dict[str, str] = dict()

        for remotePackageName, remotePackageURL in remoteIndexHRefs.items():
            if not remotePackageName in localIndexHRefs:
                resultingDict[remotePackageName] = remotePackageURL

        if not self.packageVersion:
            additionalPackagesMessage: str = self.__checkPackagesInLocalButNotInRemote(remoteIndexHRefs, localIndexHRefs)
            if additionalPackagesMessage != "":
                print("WARNING! " + additionalPackagesMessage)

        return resultingDict

    def getPackageDiff(self):
        """Synchronize the self.packageName against the PyPI remote repository, i.e. it downloads only the new packages available or, in general terms, the ones fulfiling the currently active filters."""

        ok, status, pypiRemoteIndex = self._networkManager.getLink(self._remotePypiBaseDir + self.packageName)
        if not ok:
            print(status)
        else:
            pypiRemoteIndexStr: str = pypiRemoteIndex.decode("utf-8")

        if self.printAllFileNames:
            packageFiles: List[str] = list(self._htmlManager.getHRefsList(pypiRemoteIndexStr).keys())
            self._printPackageNamesInHTML(packageFiles, "\nRetrieved package files (before filtering)")

        with open(self.packageHTMLFileFullName, "r") as pypiLocalIndexFile:
            pypiLocalIndex: str = pypiLocalIndexFile.read()

        pypiRemoteIndexFiltered: str = self._htmlManager.filterInHTML(pypiRemoteIndexStr, self._regexZIPAndTars)

        remoteIndexHRefs: Dict[str, str] = self._htmlManager.getHRefsList(pypiRemoteIndexFiltered)
        localIndexHRefs: Dict[str, str] = self._htmlManager.getHRefsList(pypiLocalIndex)
        newPackagesToDownload: Dict[str, str] = self.__getNewPackagesInRemote(remoteIndexHRefs, localIndexHRefs)

        if self.printAllFileNames:
            self._printPackageNamesInHTML(list(remoteIndexHRefs.keys()), "\nIn-the-remote package files (after filtering)")
            self._printPackageNamesInHTML(list(localIndexHRefs.keys()), "\nIn-the-local package files")
            self._printPackageNamesInHTML(list(newPackagesToDownload.keys()), "\nTo-be-downloaded package files (after filtering, in-the-remote minus in-the-local ones)")

        with open(self.packageHTMLFileFullName, "r+") as pypiLocalIndexFile:
            self._downloadFilesInLocalPath(newPackagesToDownload, pypiLocalIndex, pypiLocalIndexFile, printVerbose=self.printVerbose, showRetries=self.showRetries)


class Remove(LocalPyPIController):
    def __init__(self):
        LocalPyPIController.__init__(self)

    def parseScriptArguments(self, args: argparse.ArgumentParser):
        LocalPyPIController.parseScriptArguments(self, args)

        # 1. Set all the params we are going to use (let the ones we don't to None):
        self.dryRun = args.dryRun

        # 2. Use only the ones we have set:
        if self.dryRun:
            shutil.copytree(self.pypiLocalPath, self._dryRunsTmpDir)
            self.pypiLocalPath = self._dryRunsTmpDir

    def __removeWholePackage(self, htmlFile: TextIOWrapper):
        htmlFile.seek(0)

        _, updatedHTML = self._htmlManager.removeHTMLEntry(htmlFile.read(), "a", self.packageName)
        self._writeFileFromTheStart(htmlFile, updatedHTML)

    def __removePackages(self, htmlFile: TextIOWrapper, subPackages: List[str]):
        htmlFile.seek(0)

        updatedHTML: str = htmlFile.read()
        for subpackage in subPackages:
            _, updatedHTML = self._htmlManager.removeHTMLEntry(updatedHTML, "a", subpackage)
        
        self._writeFileFromTheStart(htmlFile, updatedHTML)

        # Actually remove the package after having updated the index
        for subpackage in subPackages:
            self._removeFile(os.path.join(self.packageLocalPath, subpackage))

    def removePackage(self):
        """Removes the specified version for the self.packageName from the local repository, or the whole package if it has not being specified. Assumes that the package exists."""

        baseHTMLFile = open(self.baseHTMLFileFullName, "r+")
        packageExist = self._htmlManager.existsHTMLEntry(baseHTMLFile.read(), "a", self.packageName)

        if not packageExist:
            print("Package '" + self.packageName + "' was not being tracked yet.")
            return

        localPackageHTMLFile = open(self.packageHTMLFileFullName, "r+")
        localPackageHTMLIndex = localPackageHTMLFile.read()
        currentLocalPackages = self._htmlManager.getHRefsList(localPackageHTMLIndex).keys()

        localSubPackagesToRemove: List[str] = list()
        for package in currentLocalPackages:
            if self.packageVersion in package:
                localSubPackagesToRemove.append(package)
        
        removeWholePackage: bool = len(localSubPackagesToRemove) == len(currentLocalPackages)
        if removeWholePackage:
            self.__removeWholePackage(baseHTMLFile)
        else:
            self.__removePackages(localPackageHTMLFile, localSubPackagesToRemove)

        # Must close files in case the whole directory (package) needs to be erased
        localPackageHTMLFile.close()
        baseHTMLFile.close()

        print("Subpackages from package '" + self.packageName + "' successfully removed:\n" + '\n'.join(localSubPackagesToRemove) + "\n")

        if removeWholePackage:
            self._removeDir(self.packageLocalPath, True)
            print("Whole package '" + self.packageName + "' successfully removed.")
            
        
class List(LocalPyPIController):
    def __init__(self):
        LocalPyPIController.__init__(self)

    def parseScriptArguments(self, args: argparse.ArgumentParser):
        LocalPyPIController.parseScriptArguments(self, args)

    def filterByVersion(self, packagesList) -> List[str]:
        resultingList: List[str] = list()
        for packageName in packagesList:
            if self.packageVersion in packageName:
                resultingList.append(packageName)

        return resultingList

    def listPackagesInTheRemote(self):
        self._htmlManager.setFlags(None, None, None, None, None, self.packageVersion)

        ok, status, pypiPackageHTML = self._networkManager.getLink(self._remotePypiBaseDir + self.packageName)
        if not ok:
            print(status)
        else:
            pypiPackageHTMLStr: str = pypiPackageHTML.decode("utf-8")

        packageFiles: List[str] = self._htmlManager.getHRefsList(pypiPackageHTMLStr).keys()

        filteredPackageFiles = self.filterByVersion(packageFiles)
        filteredPackageFiles.sort()

        print("Found " + str(len(filteredPackageFiles)) + " packages (IN THE REMOTE, i.e. NOT DOWNLOADED - perform the 'add' command to add the the package to the local repository):")
        print('\n'.join(filteredPackageFiles))

    def listPackages(self):
        """Lists all the packages in the root HTML index, if self.packageName == None. Lists the downloaded files for package self.packageName otherwise."""

        printMessage: str = ""

        htmlString: str = ""
        if self.packageName == "":
            with open(self.baseHTMLFileFullName, "r") as baseHTMLFile:
                htmlString = baseHTMLFile.read()

            printMessage = "Found {} packages:"
        else:
            with open(self.packageHTMLFileFullName, "r") as packageHTMLFile:
                htmlString = packageHTMLFile.read()

            printMessage = "Found {} files for package '" + str(self.packageVersion if self.packageVersion else self.packageName) + "':"

        packageFiles: List[str] = self._htmlManager.getHRefsList(htmlString).keys()

        filteredPackageFiles = self.filterByVersion(packageFiles)
        filteredPackageFiles.sort()
        
        print(printMessage.format(len(filteredPackageFiles)))
        print('\n'.join(filteredPackageFiles))

class Config(LocalPyPIController):
    def __init__(self):
        self._printWheelFilters: bool = None

    @property
    def printWheelFilters(self):
        return self._printWheelFilters

    @printWheelFilters.setter
    def printWheelFilters(self, new_printWheelFilters: str):
        self._printWheelFilters = new_printWheelFilters

    def parseScriptArguments(self, args: argparse.ArgumentParser):
        # 1. Set all the params we are going to use (let the ones we don't to None):
        self.printWheelFilters = args.showConfig

    def _getTextInGreen(self, text: str) -> str:
        CSI = "\x1B["
        resultingText = CSI+"32;40m" + text + CSI + "0m"

        return resultingText

    def getWheelFiltersSettings(self) -> str:
        """Gets the current settings at the settings location for the wheels filtering."""

        resultingString: str = ""

        resultingString += "Wheel filters settings file @ " + self._htmlManager.getWheelFiltersSettingsFilePath() + "\n"
        resultingString += "\n"

        filterEnabled: bool = self._htmlManager.areWheelFiltersEnabled()
        inOrOut: str = self._htmlManager.inOrOutFilterEnabled()

        resultingString += "Wheel filters enabled: " + str(filterEnabled) + " [applying=" + inOrOut + "]" + "\n"
        if self._htmlManager.areWheelFiltersEnabled():
            inFilterStr = "\n"
            inFilterStr += "\tIN filters ('" + str(self._htmlManager._wheelsManager.wheelsConfig.in_ORorAnd) + "'):\t" + str(self._htmlManager._wheelsManager.wheelsConfig.inFilters) + "\n"
            inFilterStr += "\t\t\t\t" + str(self._htmlManager._wheelsManager.wheelsConfig.in_ORorAndAttributes)

            if inOrOut == "in":
                resultingString += self._getTextInGreen(inFilterStr)
            else:
                resultingString += inFilterStr

            resultingString += "\n"

            outFilterStr = "\n"
            outFilterStr += "\tOUT filters ('" + str(self._htmlManager._wheelsManager.wheelsConfig.out_ORorAnd) + "'):\t" + str(self._htmlManager._wheelsManager.wheelsConfig.outFilters) + "\n"
            outFilterStr += "\t\t\t\t" + str(self._htmlManager._wheelsManager.wheelsConfig.out_ORorAndAttributes)

            if inOrOut == "out":
                resultingString += self._getTextInGreen(outFilterStr)
            else:
                resultingString += outFilterStr
            
            resultingString += "\n"

        return resultingString


class RebuildIndex(LocalPyPIController):
    def __init__(self):
        LocalPyPIController.__init__(self)

    def parseScriptArguments(self, args: argparse.ArgumentParser):
        LocalPyPIController.parseScriptArguments(self, args)

    def __getDirectoriesInLocal(self):
        dirsAndFileNames: List[str] = os.listdir(self.pypiLocalPath)
        return [el for el in dirsAndFileNames if el != "settings" and "index.html" not in el]

    def __rebuildMainIndex(self):
        baseHTML: str = self._htmlManager.getBaseHTML()

        directories: List[str] = self.__getDirectoriesInLocal()

        with open(self.baseHTMLFileFullName, "r+") as baseHTMLFile:
            self._addPackagesToIndex(baseHTML, baseHTMLFile, {"./" + dir:dir for dir in directories})

        print("Main index rebuilt.")

        return directories
    
    def __getSubpackagesForPackage(self, packageLocalPath: str):
        subpackagesList: List[str] = os.listdir(packageLocalPath)
        return [file for file in subpackagesList if re.match(self._regexZIPAndTars, file) or ".whl" in file]

    def __rebuildIndexForPackage(self, package: str):
        packageLocalPath: str = os.path.join(self.pypiLocalPath, package) + "/"
        packageHTMLFileFullName: str = os.path.join(packageLocalPath, self._packageHTMLFileName)

        baseHTML: str = self._htmlManager.getBaseHTML()

        subpackages: List[str] = self.__getSubpackagesForPackage(packageLocalPath)

        _, baseHTML = self._htmlManager.insertHTMLEntry(baseHTML, "h1", "Links for " + self.packageName, {})
        with open(packageHTMLFileFullName, "w") as packageHTML_file:
            self._addPackagesToIndex(baseHTML, packageHTML_file, {"./" + subpackage:subpackage for subpackage in subpackages})
        
        print("Index for '" + package + "' rebuilt.")

    def rebuildAllIndices(self):
        print()

        currentPackages: List[str] = self.__rebuildMainIndex()
        
        for package in currentPackages:
            self.__rebuildIndexForPackage(package)
    
    def rebuildIndex(self):
        print()
        
        if self.packageName == "":
            self.__rebuildMainIndex()
        else:
            self.__rebuildIndexForPackage(self.packageName)