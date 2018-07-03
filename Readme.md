# Enrollment, Bootstrapping, and the Munki Barrel. A University-wide approach.

## Projects utilized for the Syracuse University campus framework:

* Munki - [https://github.com/munki/munki](https://github.com/munki/munki)
* Munki Web Admin 2 - [https://github.com/munki/mwa2](https://github.com/munki/mwa2)
* MicroMDM - [https://github.com/micromdm/micromdm](https://github.com/micromdm/micromdm)
* InstallApplications - [https://github.com/erikng/installapplications](https://github.com/erikng/installapplications)
* DEPNotify - [https://gitlab.com/Mactroll/DEPNotify](https://gitlab.com/Mactroll/DEPNotify)

## Present workflow for enrollment
1. Unbox system & power on, or install macOS using Apple's installer.
1. Proceed through the intial setup wizard.
    1. For DEP enrolled systems, you will be notified that your organization will configure the machine. The initial admin user account can be pushed to the system as part of this process.
    1. For non-DEP systems, you will proceed through the entire setup process, and manually create the first administrative user account.
1. Part of the MDM enrollment will install a package utilizing Erik Gomez's "Install Applications" - triggering several followup installs.
1. The new packages will include Munki Tools, DEPNotify, and an initial Router enrollment package.
    1. This package reads the serial number from the system, executing a curl command which touches the enroll.py API, enrolling the machine in the Router barrel.
1. Locate the machine's manifest, by serial number, in the router barrel.
    1. Set the computer name & clientID
    1. Assign the barrel enrollment pkg 
1. Restart the machine as prompted by the DEPNotify window.
1. The system will now download the machine manifest from the router barrel, and install the barrel enrollment package. This install reads the machine name & clientID from the locally cached manifest.
1. The system is now enrolled in the individual department's munki barrel.

