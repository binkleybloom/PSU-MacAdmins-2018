# Process Munki Router Enrollers

This script can automate the creation of enrollment pkgs for munki barrels, which utilize the `enroll.py` API for manifest creation, and the specialized version of MWA2 which includes fields for ClientIdentifier and ComputerName.

To use, fill out the example csv file with the appropriate fields, and modify the marked configuration areas in both the `processEnrollers.py` and `/templateFiles/postinstall_script.py` scripts.

*Do not modify the contents of templateFIles unless you have a good understanding of how it's used.*

### `processEnrollers.py` configuration fields:
1. The path to your munki repo. This is the local path only; smb:// or similar are not recognized.
1. The pkginfo extension used by your repo.

### `postinstall_script.py` configuration fields:
1. Time zone information, discoverable [here](https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones).
2. The username/password for the ENROLLMENT API (not munki repo).

### Sample execution:
```bash
python ./processEnrollers.py --csv="barrels.csv"
```
