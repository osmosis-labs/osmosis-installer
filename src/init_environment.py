import subprocess
import os
import time
import globals
from style import bcolors
from init_setup import initSetup


def initEnvironment(args):
    if globals.selected_networktype == globals.NetworkType.MAINNET:
        globals.selected_version = globals.NetworkVersion.MAINNET.value
    if globals.selected_networktype == globals.NetworkType.TESTNET:
        globals.selected_version = globals.NetworkVersion.TESTNET.value

    if globals.os_name == "Linux":
        print(bcolors.OKGREEN + "System Detected: Linux" + bcolors.ENDC)
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        mem_gib = mem_bytes/(1024.**3)
        print(bcolors.OKGREEN + "RAM Detected: " +
              str(round(mem_gib))+"GB" + bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN + """
You have less than the recommended 32GB of RAM. Would you like to set up a swap file?
1) Yes, set up swap file
2) No, do not set up swap file
            """ + bcolors.ENDC)
            if args.swapOn == True:
                swapAns = '1'
            elif args.swapOn == False:
                swapAns = '2'
            else:
                swapAns = input(bcolors.OKGREEN +
                                'Enter Choice: ' + bcolors.ENDC)

            if swapAns == "1":
                swapNeeded = 32 - round(mem_gib)
                print(bcolors.OKGREEN + "Setting up " +
                      str(swapNeeded) + "GB swap file..." + bcolors.ENDC)
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
                print(bcolors.OKGREEN + str(swapNeeded) +
                      "GB swap file set" + bcolors.ENDC)
                initSetup(args)
            elif swapAns == "2":
                subprocess.run(["clear"], shell=True)
                initSetup(args)
            else:
                subprocess.run(["clear"], shell=True)
                initEnvironment(args)
        else:
            print(bcolors.OKGREEN + "You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..." + bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup(args)

    elif globals.os_name == "Darwin":
        print(bcolors.OKGREEN + "System Detected: Mac" + bcolors.ENDC)
        mem_bytes = subprocess.run(
            ["sysctl hw.memsize"], capture_output=True, shell=True, text=True)
        mem_bytes = str(mem_bytes.stdout.strip())
        mem_bytes = mem_bytes[11:]
        mem_gib = int(mem_bytes)/(1024.**3)
        print(bcolors.OKGREEN + "RAM Detected: " +
              str(round(mem_gib))+"GB" + bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN + """
You have less than the recommended 32GB of RAM. Would you still like to continue?
1) Yes, continue
2) No, quit
            """ + bcolors.ENDC)
            if args.swapOn == True:
                warnAns = '1'
            elif args.swapOn == False:
                warnAns = '1'
            else:
                warnAns = input(bcolors.OKGREEN +
                                'Enter Choice: ' + bcolors.ENDC)

            if warnAns == "1":
                subprocess.run(["clear"], shell=True)
                initSetup(args)
            elif warnAns == "2":
                subprocess.run(["clear"], shell=True)
                quit()
            else:
                subprocess.run(["clear"], shell=True)
                initEnvironment(args)
        else:
            print(bcolors.OKGREEN + "You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..." + bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup(args)
    else:
        print(bcolors.OKGREEN + "System OS not detected...Will continue with Linux environment assumption..." + bcolors.ENDC)
        time.sleep(3)
        initSetup(args)
