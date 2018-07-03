#!/usr/bin/env python

# Copyright 2017, Timothy Schutt.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
enroll.py

Created by Tim Schutt at Syracuse University, 2017.

An API that copies a template manifest from a specified path, placing it in
a munki repository, named for a machine.

Script is called with the curl command
$ curl -k -u username:password --data "name=NewManifestName,bu=BarrelID" https://enrollment.url/enroll.py

HTTP Basic Auth is used, and configured outside the scope of this script.

Template manifest name and barrel paths are configured below.
The template manifest is located within each barrel's manifest directory, enabling the
IT staff for each barrel to customize it for their needs.

"""

import cgitb
import cgi
import plistlib
import os

#==== Configuration block ====#

## recognized munki barrels "barrelID":"pathToRepo"
repoPaths = {  # configure dictionary with barrelID & Path - don't forget your router entry!
    "academics": "/var/vhosts/academics/httpsdocs",
    "finance": "/var/vhosts/finance/httpsdocs",
    "router": "/var/vhosts/router/httpsdocs"
}

template = "AutoGenTemplate"  # The template name. To be located within the barrel manifests directory

#===== End of Configuration block - do not edit below =====#

cgitb.enable()
form = cgi.FieldStorage()

print "Content-Type: text/html"
print

def processSubmitted(getName, repoPath):
    targetPlist = repoPath + "/manifests/" + getName
    if not os.path.isfile(targetPlist):
        f = open(targetPlist, 'wb')
        plistlib.writePlist(templatePlist, f)
        f.close
        print "Manifest " + getName + " created.\n"
    else:
        print "Manifest " + getName + " already exists and will not be overwritten.\n"

if 'name' and 'bu' in form.keys():
    businessUnit = form.getfirst("bu").lower()
    newManifest = form.getfirst("name")

    if businessUnit in repoPaths:
        Path = repoPaths[businessUnit]

    if businessUnit not in repoPaths:
        print "Business unit not configured. Exiting."
    elif not os.path.isfile(Path + '/manifests/AutoGenTemplate'):
        print "Template manifest does not exist. Exiting."
    else:
        f = open(Path + '/manifests/' + template, 'rb')
        templatePlist = plistlib.readPlist(f)
        processSubmitted(newManifest, Path)

else:
    print "Submitted data was incomplete. Exiting."