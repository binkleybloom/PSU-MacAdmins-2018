#!/usr/bin/env python

"""
This script 

It is triggered once an active network connection has been detected. 
It reads the computer name and client identifier from the client manifest, and assigns 
those values to the machine and munki preferences after installation.

Tim Schutt, taschutt@syr.edu, 2017
Syracuse University
"""

import os
import sys
import plistlib
import subprocess

#=== configure your org's settings ===#

CurTimeZone = 'America/New_York'                     # update for your localization
EnrollCredentials = 'EnrollUser:EnrollUserPassword'  # update for httpauth user on enrollment site

#=== DO NOT EDIT BELOW THIS LINE ===#


BARRELID = "_BARRELID_"  # Set the Barrel ID for the target OU - leveraged by processEnrollers.py
REPO_URL = "_REPOURL_"   # Also configured via processEnrollers.py - as are all _VARNAME_ references.

CACHEDMANIFESTPATH = "/Library/Managed Installs/manifests/"

CMD = ["/usr/sbin/system_profiler","SPHardwareDataType"]
cmd_exec = subprocess.Popen(CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(cmd_result, cmd_err) = cmd_exec.communicate()

for line in cmd_result.splitlines():
    if "Serial Number (system)" in line:
        sn = line.split()[3]

if os.path.isfile(CACHEDMANIFESTPATH + "client_manifest.plist"):
    cachedManifest = (CACHEDMANIFESTPATH + "client_manifest.plist")
elif os.path.isfile(CACHEDMANIFESTPATH + sn):
    cachedManifest = (CACHEDMANIFESTPATH + sn)
else:
    print "Expected cached manifest file not found."
    sys.exit(1)

try:
    file = plistlib.readPlist(cachedManifest)
except:
    print "Unable to load expected cached manifest."
    sys.exit(1)

clientId = file['ClientIdentifier']
computerId = file['ComputerName']
barrelEnrollData = "name=%s&bu=%s" % (clientId, BARRELID)

# Set machine specific name and munki prefs
subprocess.call(['/usr/bin/defaults','write','/Library/Preferences/ManagedInstalls.plist','ClientIdentifier',clientId])
subprocess.call(['/usr/sbin/scutil','--set','ComputerName', computerId])
subprocess.call(['/usr/sbin/scutil','--set','HostName', computerId])
subprocess.call(['/usr/sbin/scutil','--set','LocalHostName', computerId])
subprocess.call(['/usr/bin/defaults','write','/Library/Preferences/SystemConfiguration/com.apple.smb.server','NetBIOSName','-string',clientId])

# Touch the munki barrel to enroll & create the machine's manifest if necessesary, and bootstrap munki to run on next boot/loginwindow.
subprocess.call(['/usr/bin/curl', '-k', '-u', EnrollCredentials, '--data', barrelEnrollData, '_ENROLLURL_'])
subprocess.call(['/usr/bin/defaults', 'write', '/Library/Preferences/ManagedInstalls.plist', 'SoftwareRepoURL', REPO_URL])
subprocess.call(['/usr/bin/defaults', 'delete', '/Library/Preferences/ManagedInstalls.plist', 'AdditionalHttpHeaders'])
subprocess.call(['/usr/bin/touch', '/Users/Shared/.com.googlecode.munki.checkandinstallatstartup'])

# Do some stuff for SU environment configuration - timezone, NTP server
subprocess.call(['/usr/sbin/systemsetup','-settimezone',CurTimeZone])

sys.exit(0)

