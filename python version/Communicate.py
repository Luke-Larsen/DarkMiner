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

def checkVersion(BaseSite,Version,UpdateFrom,GithubLink):
    URL = BaseSite + 'coms.php'
    #Diffrent OS giving problems with os.environ. This solution worked for windows
    #I might need to check it on more platforms
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
        print(data)
    except:
        print(r)
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
                    if not data['message'].startswith("API rate limit"):
                        print(data)
                        if(int(data) > int(Version)):
                            print("Newer version found on github")
                            #TODO
                            #upgrade(ver,osSystem,GithubLink)
                        elif(int(data)==int(Version)):
                            print("No new version found on github")
                        else:
                            print("Only older versions found on github")
                    else:
                        print("API requests exceeded")
                else:
                    print("No versions on github")
            else:
                print("No github data")
        else: 
            #Set to something custom or 1
            #Allow updates from the CNC module
            print("manual updates coming soon")