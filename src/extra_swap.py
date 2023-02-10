import subprocess
import os
import time
from style import bcolors, colorprint
from replays import replayFromGenesisDb


def extraSwap(args):
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes/(1024.**3)
    colorprint("RAM Detected: "+str(round(mem_gib))+"GB")
    swapNeeded = 64 - round(mem_gib)
    if round(mem_gib) < 64:
        colorprint("""
There have been reports of replay from genesis needing extra swap (up to 64GB) to prevent OOM errors.
Would you like to overwrite any previous swap file and instead set a """+str(swapNeeded)+"""GB swap file?
1) Yes, set up extra swap (recommended)
2) No, do not set up extra swap
        """)
        if args.extraSwap == True:
            swapAns = '1'
        elif args.extraSwap == False:
            swapAns = '2'
        else:
            swapAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

        if swapAns == "1":
            colorprint("Setting up " + str(swapNeeded) + "GB swap file...")
            subprocess.run(["sudo swapoff -a"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo fallocate -l " + str(swapNeeded)+"G /swapfile"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo chmod 600 /swapfile"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo mkswap /swapfile"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo swapon /swapfile"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo cp /etc/fstab /etc/fstab.bak"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["clear"], shell=True)
            colorprint(str(swapNeeded)+"GB swap file set")
            replayFromGenesisDb(args)
        elif swapAns == "2":
            subprocess.run(["clear"], shell=True)
            replayFromGenesisDb(args)
        else:
            subprocess.run(["clear"], shell=True)
            extraSwap(args)
    else:
        colorprint(
            "You have enough RAM to meet the 64GB minimum requirement, moving on to system setup...")
        time.sleep(3)
        subprocess.run(["clear"], shell=True)
        replayFromGenesisDb(args)
