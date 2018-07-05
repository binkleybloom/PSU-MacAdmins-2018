# Munki Enroll

A python script that receives a BarrelID & target manifest name, copying a template manifest to the target name.

Barrel IDs and paths need to be configured. Template manifest name can also be customized to taste.

Create your template manifest in the manifests directory of the munki repo or target barrel, named consistently with the "template" variable on line 50 of the enroll.py script.

This script differs from the `router.py` API in that it looks for the autoGenManifest within the manifests directory - providing a method for IT staff to modify their basic machine template in Munki Web Admin.

## Apache configuration
CGI execution must be set on the directory housing the script.

Sample .htaccess file:

```apacheconf
Options +ExecCGI
AddHandler cgi-script .py

AuthName "Munki auto-enrollment area"
AuthType Basic
AuthUserFile /var/vhosts/enroll-vhost/users
require valid-user
```