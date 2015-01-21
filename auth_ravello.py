# -*- coding: utf-8 -*-
# Copyright 2015 Ravshello Authors
# License: Apache License 2.0 (see LICENSE or http://apache.org/licenses/LICENSE-2.0.html)

# Modules from standard library
from __future__ import print_function
from getpass import getpass
import sys

# Custom modules
try:
    import ravello_sdk
    ravello_sdk.is_rsaw_sdk()
except:
    print("Missing proper version of required python module (rsaw's ravello_sdk)\n"
          "Get it from https://github.com/ryran/python-sdk/tree/experimental\n")
    raise


def get_username(prompt="Enter username: ", defaultUser=None):
    """Prompt for a username, allowing pre-populated *defaultUser*."""
    user = raw_input(prompt)
    while not len(user):
        if defaultUser:
            user = defaultUser
        else:
            user = raw_input("    You must enter a username: ")
    return user


def get_passphrase(prompt="Enter passphrase: ", defaultPass=None):
    """Prompt for a passphrase, allowing pre-populated *defaultPass*."""
    passwd = getpass(prompt)
    while not len(passwd):
        if defaultPass:
            passwd = defaultPass
        else:
            passwd = getpass("    You must enter a passphrase: ")
    return passwd


def login(ravshOpt):
    """Determine Ravello credentials and login via RavelloClient object"""
    c = ravshOpt.c
    # Create client object
    ravClient = ravello_sdk.RavelloClient()
    c.verbose("\nConnecting to Ravello . . .")
    cfgUser = ravshOpt.cfgFile.get('ravelloUser', None)
    cfgPass = ravshOpt.cfgFile.get('ravelloPass', None)
    cfgMesg = ravshOpt.cfgFile.get('unableToLoginAdditionalMsg', None)
    # If necessary, get Ravello *username* from configfile or prompt
    if not ravshOpt.ravelloUser:
        if cfgUser:
            ravshOpt.ravelloUser = cfgUser
        else:
            ravshOpt.ravelloUser = get_username(
                c.CYAN("  Enter Ravello username: "))
    # If necessary, get Ravello *password* from configfile or prompt
    if not ravshOpt.ravelloPass:
        if cfgPass:
            ravshOpt.ravelloPass = cfgPass
        else:
            ravshOpt.ravelloPass = get_passphrase(
                c.CYAN("  Enter Ravello passphrase: "))
    try:
        ravClient.login(ravshOpt.ravelloUser, ravshOpt.ravelloPass)
    except:
        print(c.RED("  Logging in to Ravello failed!"))
        print("\nIf you're sure your Ravello credentials are correct, "
              "try updating ravshello")
        if cfgMesg: print(cfgMesg)
        sys.exit(5)
    print(c.GREEN("  Logged in to Ravello as "), end='')
    if ravshOpt.enableAdminFuncs:
        print(c.YELLOW("ADMIN"), end="")
        if ravshOpt.showAllApps:
            print(" " + c.bgRED("[global app visiblity]"))
        else:
            print()
    else:
        print(c.GREEN("LEARNER"))
    return ravClient
