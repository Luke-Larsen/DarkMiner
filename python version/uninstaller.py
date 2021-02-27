import sys

if sys.platform.startswith('win32'):
    #Kill any live versions
    #Destroy startup script
    #Cleanup appdata files
    #Remove program files


elif sys.platform.startswith('linux'):
    #Disable Systemd service
    #Remove our systemd services
    #Kill running version
    #Destroy program files