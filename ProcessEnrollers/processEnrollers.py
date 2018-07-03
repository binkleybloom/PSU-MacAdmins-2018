#!/usr/bin/env python

"""

This tool creates munki barrel enrollment packages that will read settings from a munki-router
manifest .plist, assign a machine to a barrel, updates the authentication string for said barrel,
names, sets the client identifier and touches the online script to create the base manifest.abs

This requires the templateFiles directory populates with the custom ManagedInstalls.plist 
and postinstall_script.py files - to be packages and leveraged in the munki deployment.

Tim Schutt, Syracuse University
taschutt@syr.edu
September, 2017

CSV file format should be 

1st row -- header row
BarrelID, BarrelURL, AuthString, pkg version, Developer Signing ID

$ python ./processEnrollers.py --csv="./barrels.csv"

"""

import subprocess
from subprocess import PIPE
import os
import sys
import csv
import argparse
import shutil
from plistlib import readPlist, writePlist

##### Configure for your environment #####
repoURL = "/Users/Shared/repo/" # path to your repository
pkginfoExtension = ".plist"
##### End of configuration #####

if not os.path.isfile("./templateFiles/ManagedInstalls.plist") or not os.path.isfile("./templateFiles/postinstall_script.py"):
    print "Template file resources are missing. Exiting."
    sys.exit(1)

parser = argparse.ArgumentParser(description='Generate a set of munki barrel enrollment packages and postinstall scripts.')
parser.add_argument('--csv', help='Path to CSV file containing barrel information. Required.')
args = parser.parse_args()

f = open("./templateFiles/ManagedInstalls.plist")
templatePlist = readPlist(f)
f.close()

tf = open('./templateFiles/postinstall_script.py')
templatePostInstall = tf.read()
tf.close()


if args.csv:
    with open(args.csv, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader, None) #skipping the header row

        # Build the authentication plist and postinstall script
        for row in reader:
            if os.path.exists(row[0]):
                shutil.rmtree(row[0])
            try:
                os.makedirs(row[0] + "/root/var/root/Library/Preferences")
            except:
                pass

            newPlist = dict(templatePlist)
            newPostInstall = templatePostInstall
            signingID = row[4]

            # modify the plist with the barrel's http authentication string
            newPlist['AdditionalHttpHeaders'] = [row[2]]

            # modify the postinstall script with Barrel ID & URL information
            newPostInstall = newPostInstall.replace("_BARRELID_", row[0])
            newPostInstall = newPostInstall.replace("_REPOURL_", row[1])
            newPostInstall = newPostInstall.replace("_HTTPLOGIN_", row[2])
            newPostInstall = newPostInstall.replace("_PASSWORD_", row[3])
            newPostInstall = newPostInstall.replace("_ENROLLURL_", row[5])

            newPlistName = "./" + row[0] + "/root/var/root/Library/Preferences/ManagedInstalls.plist"
            newPostInstallName = "./" + row[0] + "/postinstall_script.py"

            # write the new plist
            f = open(newPlistName, 'wb')
            writePlist(newPlist, f)
            f.close()

            # write the new postinstall script
            f = open(newPostInstallName, 'w')
            f.write(newPostInstall)
            f.close()
            
            # build & sign installation pkg

            pkgTempName = './' + row[0] + '/' + row[0] + '-BarrelEnroll-' + row[3] + '-temp.pkg'
            pkgFinalName = './' + row[0] + '/' + row[0] + '-BarrelEnroll-' + row[3] + '.pkg'
            pkgbuildCmd = ['/usr/bin/pkgbuild','--root', row[0] + '/root', 
                           '--identifier','com.github.binkleybloom.' + row[0] + '-BarrelEnroll',
                           '--version', row[3], pkgTempName]

            productSignCmd = ['/usr/bin/productsign', '--sign', signingID, pkgTempName, pkgFinalName]

            subprocess.call(pkgbuildCmd)
            subprocess.call(productSignCmd)

            # Make pkginfo file for Munki
            pkginfoCmd = ['/usr/local/munki/makepkginfo',pkgFinalName,'--postinstall_script', row[0] + '/postinstall_script.py',\
                          '--catalog','production']

            pkginfoCall=subprocess.Popen(pkginfoCmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (pkginfoFile, error) = pkginfoCall.communicate()

            f= open(pkgFinalName + pkginfoExtension,'wb')
            f.write(pkginfoFile)
            f.close()

            # copy pkginfo and installer into router munki repository
            subprocess.call(['cp',pkgFinalName,repoURL + 'pkgs/'])
            subprocess.call(['cp',pkgFinalName + pkginfoExtension,repoURL + 'pkgsinfo/'])

            os.remove(pkgTempName)
            os.remove(row[0] + '/postinstall_script.py')
            #shutil.rmtree(row[0] + '/root')

    subprocess.call(['/usr/local/munki/makecatalogs', repoURL])

sys.exit(0)