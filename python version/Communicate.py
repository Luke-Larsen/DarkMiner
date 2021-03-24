import configparser,os,requests,multiprocessing

def startSignal(BaseSite):
    URL = BaseSite + 'coms.php'
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') +'/bin/DarkMiner/'+"config.ini")
    TotalTimeMining = config['value']['TotalTimeMining']
    #Diffrent OS giving problems with os.environ. This solution worked for windows
    #I might need to check it on more platforms
    try:
        PARAMS = {'Type':'startSignal','name': os.environ['USER'], 'CPU': multiprocessing.cpu_count(),'Mining':1,'MiningTotalTime':TotalTimeMining}
    except KeyError as e:
        print('Computer no work right: "%s"' % str(e))
        try:
            PARAMS = {'Type':'startSignal','name': os.getlogin(), 'CPU': multiprocessing.cpu_count(),'Mining':1,'MiningTotalTime':TotalTimeMining}
        except KeyError as e:
            print('Computer really no work right: "%s"' % str(e))
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    print(data)

def endSignal(BaseSite):
    URL = BaseSite + 'coms.php'
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') +'/bin/DarkMiner/'+"config.ini")
    TotalTimeMining = config['value']['TotalTimeMining']
    try:
        PARAMS = {'Type':'endSignal','name': os.environ['USER'], 'CPU': multiprocessing.cpu_count(),'Mining':0,'MiningTotalTime':TotalTimeMining}
    except KeyError as e:
        print('Computer no work right: "%s"' % str(e))
        try:
            PARAMS = {'Type':'endSignal','name': os.getlogin(), 'CPU': multiprocessing.cpu_count(),'Mining':0,'MiningTotalTime':TotalTimeMining}
        except KeyError as e:
            print('Computer really no work right: "%s"' % str(e))
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    print(data)

def checkVersion(BaseSite,Version,UpdateFrom,GithubLink):
    URL = BaseSite + 'coms.php'
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
        if not UpdateFrom: 
            #If not set or set to default check github for update 
            #Check github for a newer version of the script
            githubReleaseLink = GithubLink + "/releases/latest"
            headers = {
                    'accept': 'application/vnd.github.v3+json'
                }
            r = requests.get(url=githubReleaseLink,headers=headers)
            data = r.json()
            if(data):
                if not data['message'] == "Not Found":
                    print(data)
                    if(int(data) > int(Version)):
                        print("Newer version found on github")
                    elif(int(data)==int(Version)):
                        print("No new version found on github")
                    else:
                        print("Only older versions found on github")
                else:
                    print("No versions on github")
            else:
                print("No github data")
        else: #Set to something custom or 1
            #Allow updates from the CNC module
            print("Coming soon")