from functions import LinuxIdleTime

def UpdateTotalMiningTime(value):
    import configparser,os
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~') +'/.darkminer/'+"config.ini")
    TotalTimeMining = config['value']['TotalTimeMining']
    NewTotalTimeMining = int(TotalTimeMining) + int(value)
    config['value'] = {
        'TotalTimeMining' : NewTotalTimeMining
    }
    with open(os.path.expanduser('~') +'/.darkminer/config.ini', 'w+') as configfile:
        config.write(configfile)

def LinuxMine64(LinuxPathDownloads,SHA256ProgramDefault,SHA256Program,waitTime,Communication,BaseSite):
    global processPid
    import os, subprocess,time,requests
    from Communicate import downTimeSignal
    if not os.path.exists(LinuxPathDownloads):
        os.mkdir(LinuxPathDownloads)
    #Switch this over to using the xmrig github repos.
    if not os.path.exists(LinuxPathDownloads+'/xmrig'):
        os.mkdir(LinuxPathDownloads+'/xmrig')
    if os.path.exists(LinuxPathDownloads + '/xmrig/xmrig'):
        print('mining binary exists no need to download')
    else:
        from functions import DownloadData
        #grab the github data and then download the latest version and update the sha256Sums
        githubReleaseLink ="https://api.github.com/repos/xmrig/xmrig/releases/latest"
        headers = {
                'accept': 'application/vnd.github.v3+json'
            }
        r = requests.get(url=githubReleaseLink,headers=headers)
        data = r.json()
        NewestMinerVersion = data['tag_name']
        DownloadMinerURL = 'https://github.com/xmrig/xmrig/releases/download/'+NewestMinerVersion+'/xmrig-'+NewestMinerVersion[1:]+'-linux-x64.tar.gz'
        print(DownloadMinerURL)
        DownloadData(DownloadMinerURL, LinuxPathDownloads + 'xmrig-linux-x64.tar.gz')
        #Extract the tar
        import tarfile
        my_tar = tarfile.open(LinuxPathDownloads + 'xmrig-linux-x64.tar.gz')
        my_tar.extractall(LinuxPathDownloads + '/xmrig/') # specify which folder to extract to
        my_tar.close()
        #Check the SHA256 against github


        # import hashlib
        # sha256_hash = hashlib.sha256()
        # with open(LinuxPathDownloads+'xmrigcg',"rb") as f:
        #     # Read and update hash string value in blocks of 4K
        #     for byte_block in iter(lambda: f.read(4096),b""):
        #         sha256_hash.update(byte_block)
        #     if sha256_hash.hexdigest() != SHA256Program:
        #         errorOccurred("HASH MISMATCH"); 


        #Move the binary to run it
        os.rename(LinuxPathDownloads+"/xmrig/"+"xmrig-"+NewestMinerVersion[1:]+"/xmrig", LinuxPathDownloads+"xmrigcg")
    
    if os.path.exists(LinuxPathDownloads + 'config.json'):
        print('config exists no need to download')
    else:
        DownloadData(BaseSite + 'Linux/' + 'config.json', LinuxPathDownloads + 'config.json')


    os.chmod(LinuxPathDownloads+"xmrigcg", 0o777)
    proc = subprocess.Popen([LinuxPathDownloads + "xmrigcg"], stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,bufsize=1,universal_newlines=True,preexec_fn=os.setsid)
    processPid = proc.pid
    TotalSleepTime = 0
    ReadHash = 0
    paused = 0
    print("Starting downtime program")
    #It will probably be a good idea to offer an option where we just send a P keypress to pause the shell
    while True:
        result = subprocess.run(['xprintidle'], stdout=subprocess.PIPE)
        IdleTimeSet = int(float(result.stdout)) / 1000
        if waitTime <= IdleTimeSet:
            #resume miner if it was paused
            if(paused):
                print('Resuming Mining')
                proc.stdin.write('r')
                proc.stdin.flush() 
            print('No activity')
            #Testing a way to see hashrates
            # if TotalSleepTime > 120 and ReadHash==0:
            #     print("trying to get hashrate")
            #     proc.stdin.write('h')
            #     proc.stdin.flush()
            #     HashRate = []
            #     #count = sum(1 for line in proc.stdout)
            #     i = 0
            #     #print(count)
            #     while i < 50:
            #         line = proc.stdout.readline()
            #         HashRate.append(line)
            #         i+=1
            #     #remove color data
            #     NonListHasRate =' '.join(HashRate)
            #     print(NonListHasRate)
            #     ReadHash = 1


            time.sleep(3)
            TotalSleepTime += 3
        else:
            print('Activity! Eject!')
            #os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # Send the signal to all the process groups
            #pause the miner instead of killing it
            print('Pausing Mining')
            proc.stdin.write('p')
            proc.stdin.flush()
            #log Total Time active
            UpdateTotalMiningTime(TotalSleepTime)
            TotalSleepTime = 0
            if Communication == 2:
                downTimeSignal(BaseSite,0)
            
            #Instead of breaking just call idle check again
            paused = 1
            LinuxIdleTime(waitTime)
            #break

def Kill():
    from os import killpg, getpgid
    from signal import SIGTERM
    try:
        if(processPid):
            killpg(getpgid(processPid), SIGTERM)  # Send the signal to all the process groups
            print("Killed Miner")
        else:
            print("No Miner")
    except NameError:
        print("No miner started")