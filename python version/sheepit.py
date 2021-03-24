def LinuxRender64(LinuxPathDownloads,waitTime,Communication,BaseSite):
    global processPid
    import os,requests,json,subprocess,time
    from functions import DownloadData
    path = LinuxPathDownloads
    #Download sheepit Client
    if not os.path.exists(LinuxPathDownloads+'/sheepit'):
        os.mkdir(LinuxPathDownloads+'/sheepit')
    if os.path.exists(LinuxPathDownloads + '/sheepitClient.jar'):
        print('sheepit binary exists no need to download')
    else:
        from functions import DownloadData
        #grab the github data and then download the latest version
        githubReleaseLink ="https://api.github.com/repos/laurent-clouet/sheepit-client/releases/latest"
        headers = {
                'accept': 'application/vnd.github.v3+json'
            }
        r = requests.get(url=githubReleaseLink,headers=headers)
        data = r.json()
        NewestRenderVersion = data["name"]
        NewestRenderDownload = data['tarball_url']
        DownloadData(NewestRenderDownload, LinuxPathDownloads + '/sheepitDownload')
        import tarfile
        my_tar = tarfile.open(LinuxPathDownloads + "/sheepitDownload")
        my_tar.extractall(LinuxPathDownloads + 'sheepit/'+NewestRenderVersion+'/') # specify which folder to extract to
        my_tar.close()
        path += 'sheepit/'+NewestRenderVersion+'/'
        from os import walk
        f = []
        for (dirpath, dirnames, filenames) in walk(path):
            f.extend(dirnames)
            break
        path += str(f[0])
        #Compile if needed
        subprocess.call(['./gradlew', 'shadowJar'],cwd=path)
        #move now created jar to working directory
        os.rename(path+"/build/libs/sheepit-client-all.jar", LinuxPathDownloads + "sheepitClient.jar")

    #Run Sheepit Client
    proc = subprocess.Popen(["java -jar sheepitClient.jar -ui text -login Jetpower1 -password hM5HZhCvQ5szZVacg7enIFiSjut3u0dXVpH3vufp"], stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,bufsize=1,universal_newlines=True,preexec_fn=os.setsid,cwd=LinuxPathDownloads)
    processPid = proc.pid
    if(processPid):
        print("Process Open")
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
                proc.stdin.write('resume')
                proc.stdin.flush() 
                paused = 0
                
            #print('No activity')
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
            proc.stdin.write('pause')
            proc.stdin.flush()
            time.sleep(3)

            #DEBUG Read out the last 8 lines to make sure everything working right
            i = 0
            DebugLines = []
            while i < 8:
                line = proc.stdout.readline()
                DebugLines.append(line)
                i+=1
            #remove color data
            NonListHasRate =' '.join(DebugLines)
            print(NonListHasRate)
            #log Total Time active
            from functions import UpdateTotalMiningTime,LinuxIdleTime
            from Communicate import endSignal
            UpdateTotalMiningTime(TotalSleepTime)
            TotalSleepTime = 0
            if Communication == 2:
                endSignal(BaseSite)
            
            #Instead of breaking just call idle check again
            paused = 1
            LinuxIdleTime(waitTime)


    #Stop Sheepit Client
def Kill():
    from os import killpg, getpgid
    from signal import SIGTERM
    try:
        if(processPid):
            killpg(getpgid(processPid), SIGTERM)  # Send the signal to all the process groups
            print("Killed Renderer Base")
        else:
            print("No Renderer Base")
    except NameError:
        print("No renderer base started")