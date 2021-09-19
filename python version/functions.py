def DownloadData(url, direc):
    import requests
    print('Beginning file download with requests')
    r = requests.get(url)
    with open(direc, 'wb') as f:
        f.write(r.content)
        print('Success Downloading files')

def upgrade(ver,osSystem,GithubLink):
    #TODO create,test,debug
    #Download from github
    githubReleaseLink = GithubLink + "/releases/latest"
    headers = {
            'accept': 'application/vnd.github.v3+json'
        }
    r = requests.get(url=githubReleaseLink,headers=headers)
    data = r.json()
    NewestVersion = data['tag_name']
    DownloadMinerURL = GithubLink + '/releases/download/'+NewestVersion+'/darkminer-'+NewestVersion+'.zip'
    print(DownloadMinerURL)
    DownloadData(DownloadMinerURL, LinuxPathDownloads + 'update.zip')
    #check SHA256
        #TODO upgrade to full pgp
    
    #unzip file
    import zipfile
    with zipfile.ZipFile(LinuxPathDownloads+'update.zip', 'r') as zip_ref:
        zip_ref.extractall(LinuxPathDownloads+'unzipped')

    #create batch or bash *Update* script to move stuff to final locations and start new program
    if osSystem == 'win32':
        print('Code for windows in progress')
    elif osSystem == 'Linux':
        update = open('updater.sh', 'w')
        update.write('mv unzipped/* *')
        update.close()
    #run script

def LinuxIdleTime(waitTime):
    import subprocess,time
    #Wayland errors were caused by something else. IdleMonitor can and probably will be used again just not changed in this update
    #Update to the previous message: While IdleMonitor can work on some machines xprintidle works better on a larger variety of machines,
    #so I am going to keep it until I either write my own or something requires me to change.
    result = subprocess.run(['xprintidle'], stdout=subprocess.PIPE)
    IdleTimeSet = result.stdout
    print("Waiting for lack of input...")
    while True:
        result = subprocess.run(['xprintidle'], stdout=subprocess.PIPE)
        #print(result.stdout)
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

def UpdateTotalMiningTime(value):
    import configparser,os
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') +'/bin/DarkMiner/'+"config.ini")
    TotalTimeMining = config['value']['TotalTimeMining']
    NewTotalTimeMining = int(TotalTimeMining) + int(value)
    config['value'] = {
        'TotalTimeMining' : NewTotalTimeMining
    }
    with open(os.path.expanduser('~') +'/bin/DarkMiner/config.ini', 'w+') as configfile:
        config.write(configfile)