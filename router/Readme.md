# Munki Router Enrollment API

A python script that receives the target manifest name (intended as the machine serial number), copying a template manifest to the target name.

This script differs from the `enroll.py` API in that it searches for the autoGenManifest outside of the munki repo web path - this prevents non munki admins from modifying the specialized machine template in Munki Web Admin.

Place the script in the root of the router repository web directory, e.g. `/var/vhosts/router/httpsdocs/router.py`, and the AutoGenTemplate.plist outside of the manifests directory to prevent modification. Path to the template must be set in the `router.py` script.

The following should be also placed in that directory for CGI configuration & authentication.

## Apache configuration
CGI execution must be set on the directory housing the script.

Sample .htaccess file:

```apacheconf
Options +ExecCGI
AddHandler cgi-script .py

AuthName "Munki auto-enrollment area"
AuthType Basic
AuthUserFile /var/vhosts/router-vhost/users
require valid-user
```

The Munki Router system uses a modified version of MunkiWebAdmin2 with a simplified manifest landing screen, available [here](https://github.com/binkleybloom/mwa2).