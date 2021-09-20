import configparser,os,requests,multiprocessing

def downTimeSignal(BaseSite,state):
    URL = BaseSite + 'coms.php'
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') +'/.darkminer/'+"config.ini")
    TotalTimeMining = config['value']['TotalTimeMining']
    Version = config['server']['Version']

    if state == 0:
        signal = 'endSignal'
    elif state == 1:
        signal = 'startSignal'
    try:
        PARAMS = {'Type':signal,'name': os.environ['USER'], 'CPU': multiprocessing.cpu_count(),'Mining':state,'MiningTotalTime':TotalTimeMining,'version':Version}
    except KeyError as e:
        print('Error with os.environ[USER] : "%s"' % str(e))
        try:
            PARAMS = {'Type':signal,'name': os.getlogin(), 'CPU': multiprocessing.cpu_count(),'Mining':state,'MiningTotalTime':TotalTimeMining,'version':Version}
        except KeyError as e:
            print('Error with os.getlogin() : "%s"' % str(e))
    r = requests.get(url=URL, params=PARAMS)
    try:
        data = r.json()
        print(data)
    except:
        print(r)

def checkVersion(Version,BaseSite,osSystem,GithubLink):
    URL = BaseSite + 'coms.php'
    #Diffrent OS giving problems with os.environ. This solution worked for windows
    #I might need to check it on more platforms
    config = configparser.ConfigParser()
    if os.path.isfile(os.path.expanduser('~') +'/.darkminer/'+"config.ini"):
        config.read(os.path.expanduser('~') +'/.darkminer/'+"config.ini")
        UpdateFrom = config['settings']['UpdateFrom']
        LinuxPathDownloads = config['settings']['LinuxPathDownloads']
    try:
        PARAMS = {'Type':'checkVersion','name': os.environ['USER']}
    except KeyError as e:
        print('Error with os.environ[USER] : "%s"' % str(e))
        try:
            PARAMS = {'Type':'checkVersion','name': os.getlogin()}
        except KeyError as e:
            print('Error with os.getlogin() : "%s"' % str(e))
    r = requests.get(url=URL, params=PARAMS)
    try: #Sometimes issues occure with json sorting it out
        data = r.json()
        #print(data)
    except:
        print(r)

    #UpdateFrom 0 is staying up to date with the latest github version
    #UpdateFrom 1 is getting the version the CNC states from github (You can set a specfic version from github on the CNC and it will stay on that one)
    #UpdateFrom 2 only updates from the CNC server and CNC version

    from functions import upgrade
    if UpdateFrom == '0': 
        #Check github for a newer version of the script
        githubReleaseLink = GithubLink + "/releases/latest"
        headers = {
                'accept': 'application/vnd.github.v3+json'
            }
        r = requests.get(url=githubReleaseLink,headers=headers)
        data = r.json()

        if(data):
            #if not data['message'] == "Not Found":
            #    if not data['message'].startswith("API rate limit"):
                    #print(data)
                    NewestVersion = float(data['tag_name'][1:])
                    if(NewestVersion > float(Version)):
                        print("Newer version found on github")
                        upgrade(NewestVersion,osSystem,LinuxPathDownloads,GithubLink)
                    elif(float(NewestVersion)==float(Version)):
                        print("No new version found on github")
                    else:
                        print("Only older versions found on github")
            #     else:
            #         print("API requests exceeded")
            # else:
            #     print("No versions on github")
        else:
            print("No github data")
    elif UpdateFrom == '1':
        if int(data) != int(Version):
            CNCVersion = int(data)
            print("CNC wants a diffrent version")
            
            upgrade(CNCVersion,osSystem,LinuxPathDownloads,GithubLink)

    elif UpdateFrom == '2':
        #Allow updates from the CNC server only
        print("manual updates coming soon")