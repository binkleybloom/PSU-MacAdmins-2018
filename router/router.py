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
router.py

This CGI script accepts a serial number POST variable from a custom .pkg installer,
generating a manifest from a prebuilt template - copying to a new manifest named
the relevent machine's serial number.
"""

import cgitb
import cgi
import plistlib
import os

## path to your template manifest ##
template = "/var/vhosts/munkiRouter/template.plist" # place the router template outside of the manifests directory
### do not edit outside this area ###

cgitb.enable()
FORM = cgi.FieldStorage()
CWD = os.getcwd()

print "Content-Type: text/html"
print

def process_submitted(getname, repopath):
    """reads template plist, writes copy to manifest named via POST data"""

    templateplist = plistlib.readPlist(template)

    targetplist = repopath + "/manifests/" + getname
    if not os.path.isfile(targetplist):
        filetwo = open(targetplist, 'wb')
        plistlib.writePlist(templateplist, filetwo)
        filetwo.close()
        print "Manifest " + getname + " created."
    else:
        print "Manifest " + getname + " already exists and will not be overwritten.\n"

if 'name' in FORM.keys():
    NEWMANIFEST = FORM.getfirst("name")
    process_submitted(NEWMANIFEST, CWD)

else:
    print "Submitted data was incomplete. Exiting."
