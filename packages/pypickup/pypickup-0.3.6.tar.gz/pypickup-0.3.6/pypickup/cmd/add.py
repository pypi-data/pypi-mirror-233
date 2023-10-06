import argparse
import os

from typing import List

from pypickup.controller import Add


class AddEP:
    @staticmethod
    def init_subparser(parser: argparse.ArgumentParser):
        parser.add_argument("packageNameList", type=str, nargs="+", default="", help="Python packages list to add to the local repository. E.g. 'numpy', 'scipy pandas', 'numpy==1.8 tensorflow=1.12.2'.")
        parser.add_argument("-p", "--index-path", dest="pypiLocalPath", type=str, default=os.getenv("PYPICKUP_INDEX_PATH", default="./.pypickup/"), help="Local root path in which the package from the PyPI repository will be downloaded.")

        parser.add_argument("-r", "--requirements", dest="packageIsRequirementsFile", default=False, action="store_true", help="Used to indicate that the input is a requirements file instead of a package or list of packages.")

        parser.add_argument("--df", "--print-default-config", dest="printDefaultConfig", default=False, action="store_true", help="Prints the default settings.")
        parser.add_argument("-a", "--print-all-file-names", dest="printAllFileNames", default=False, action="store_true", help="Prints all the package files before being filtered whatsoever, prints the ones being filtered and finally prints the resulting subset that will be actually downloaded.")
        parser.add_argument("-v", "--verbose", dest="printVerbose", default=False, action="store_true", help="Prints the downloads in a more verbose fashion. WARNING! It slows down the execution.")
        parser.add_argument("--show-retries", dest="showRetries", default=False, action="store_true", help="Shows the retries in case there are any (e.g. due to a faulty network connection.")

        parser.add_argument("-s", "--only-src", dest="onlySources", default=False, action="store_true", help="Download only the source files (.zip and .tar.gz). Disabled by default.")
        parser.add_argument("--dev", dest="includeDevs", default=False, action="store_true", help="Download also the new development releases (alpha, betas), which are not included by default.")
        parser.add_argument("--rc", dest="includeRCs", default=False, action="store_true", help="Download also the release candidates (rc), which are not included by default.")
        parser.add_argument("--ps", "--platform-specific", dest="includePlatformSpecific", default=False, action="store_true", help="Download also the platform-specific wheels, which are not included by default. If this flag is not set, only platform-agnostic files are considered (-any.whl).")
        
        parser.add_argument("-d", "--dry-run", dest="dryRun", default=False, action="store_true", help="Display the changes that would be performed without actually making them. Can be combined with the printing options in order to know what is the exact behaviour. E.g. pypickup add -d --nf numpy.")

    @staticmethod
    def run(args: argparse.Namespace):
        listOfPackages: List[str] = args.packageNameList
        if args.packageIsRequirementsFile:

            requirementsFile = ''.join(listOfPackages)
            listOfPackages = []
            with open(requirementsFile, "r") as reqsFile:
                listOfPackages.extend(package.strip("\r\n") for package in reqsFile.readlines())

        for packageName in listOfPackages:

            args.packageName = packageName

            controllerInstance = Add()
            controllerInstance.parseScriptArguments(args)

            controllerInstance.printDefaultConfigIfRequired()

            print("Adding '" + packageName + "' to the local index (" + os.path.abspath(args.pypiLocalPath) + "/" + "):")
            if controllerInstance.validPackageName():
                controllerInstance.initLocalRepo()

                if not controllerInstance.packageExists():
                    controllerInstance.addNewPackageToIndex()
                    controllerInstance.getPackage()
                else:
                    controllerInstance.getPackageDiff()
            else:
                print("Package " + controllerInstance.packageName + " does not exist in the remote repository (" + controllerInstance.remotePyPIRepository + ")")

            print()
