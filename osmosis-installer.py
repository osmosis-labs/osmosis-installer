import subprocess
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def completeCosmovisor ():
    subprocess.run(["clear"], shell=True)
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")   
    print(bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: sudo systemctl status cosmovisor")
    print(bcolors.OKGREEN + "To see the live logs from cosmovisor, run the following command: journalctl -u cosmovisor -f")


def completeOsmosisd ():
    subprocess.run(["clear"], shell=True)
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")   
    print(bcolors.OKGREEN + "To see the status of the osmosis daemon, run the following command: sudo systemctl status osmosisd")
    print(bcolors.OKGREEN + "To see the live logs from the osmosis daemon, run the following command: journalctl -u osmosisd -f")


def cosmovisorInit ():
    subprocess.run(["clear"], shell=True)
    HOME = subprocess.run(["echo $HOME"], capture_output=True, shell=True, text=True)
    GOPATH = subprocess.run(["echo $GOPATH"], capture_output=True, shell=True, text=True)
    USER = subprocess.run(["echo $USER"], capture_output=True, shell=True, text=True)
    print(bcolors.OKGREEN + """Do you want to use Cosmovisor to automate future upgrades?
1) Yes
2) No
    """)
    useCosmovisor = input(bcolors.OKGREEN + 'Enter Choice: ')
    if useCosmovisor == "1":
        print(bcolors.OKGREEN + "Setting Up Cosmovisor" + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME.stdout.strip()))
        subprocess.run(["git clone https://github.com/cosmos/cosmos-sdk"], shell=True)
        os.chdir(os.path.expanduser(HOME.stdout.strip()+'/cosmos-sdk'))
        subprocess.run(["git checkout v0.44.0 && make cosmovisor"], shell=True)
        subprocess.run(["cp cosmovisor/cosmovisor "+ GOPATH.stdout.strip()+"/bin/cosmovisor"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis/bin"], shell=True)
        subprocess.run(["mkdir -p "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/upgrades"], shell=True)
        subprocess.run(["echo '# Setup Cosmovisor' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_NAME=osmosisd' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_HOME="+ HOME.stdout.strip()+"/.osmosisd' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)    
        subprocess.run(["echo 'export DAEMON_ALLOW_DOWNLOAD_BINARIES=false' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export DAEMON_LOG_BUFFER_SIZE=512' >> "+ HOME.stdout.strip()+"/.profile"], shell=True) 
        subprocess.run(["echo 'export DAEMON_RESTART_AFTER_UPGRADE=true' >> "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["echo 'export UNSAFE_SKIP_BACKUP=true' >> "+ HOME.stdout.strip()+"/.profile"], shell=True) 
        subprocess.run(["source "+ HOME.stdout.strip()+"/.profile"], shell=True)
        subprocess.run(["cp "+ GOPATH.stdout.strip()+"/bin/osmosisd "+ HOME.stdout.strip()+"/.osmosisd/cosmovisor/genesis/bin"], shell=True)     
        print(bcolors.OKGREEN + "Creating Cosmovisor Service" + bcolors.ENDC)
        subprocess.run(["""echo '[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_HOME="""+ HOME.stdout.strip()+"""/.osmosisd\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
Environment=\"UNSAFE_SKIP_BACKUP=true\"
User="""+ USER.stdout.strip()+"""
ExecStart="""+ HOME.stdout.strip()+"""/go/bin/cosmovisor start
Restart=always
RestartSec=3
LimitNOFILE=4096
[Install]
WantedBy=multi-user.target
' >cosmovisor.service
        """], shell=True)
        subprocess.run(["sudo mv cosmovisor.service /lib/systemd/system/cosmovisor.service"], shell=True)
        subprocess.run(["sudo systemctl daemon-reload"], shell=True)
        subprocess.run(["sudo systemctl start cosmovisor"], shell=True)
        completeCosmovisor()
    elif useCosmovisor == "2":
        print(bcolors.OKGREEN + "Creating Cosmovisor Service" + bcolors.ENDC)
        subprocess.run(["""echo '[Unit]
Description=Osmosis Daemon
After=network-online.target
[Service]
User="""+ USER.stdout.strip()+"""
ExecStart=$(which osmosisd) start
Restart=always
RestartSec=3
LimitNOFILE=4096
Environment=\"DAEMON_HOME="""+ HOME.stdout.strip()+"""/.osmosisd\"
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
[Install]
WantedBy=multi-user.target
' >osmosisd.service
        """], shell=True)
        subprocess.run(["sudo mv osmosisd.service /lib/systemd/system/osmosisd.service"], shell=True)
        subprocess.run(["sudo systemctl daemon-reload"], shell=True)
        subprocess.run(["sudo systemctl start osmosisd"], shell=True)
        completeOsmosisd() 
    else:
        print ("Wrong selection, try again")
        cosmovisorInit()



def snapshotInstall ():
    subprocess.run(["clear"], shell=True)
    print(bcolors.OKGREEN + "Downloading Decompression Packages" + bcolors.ENDC)
    subprocess.run(["sudo apt-get install wget liblz4-tool aria2 -y"], shell=True)
    print(bcolors.OKGREEN + "Downloading Snapshot" + bcolors.ENDC)
    proc = subprocess.run(["curl https://quicksync.io/osmosis.json|jq -r '.[] |select(.file==\""+ fileName +"\")|select (.mirror==\""+ location +"\")|.url'"], capture_output=True, shell=True, text=True)
    os.chdir(os.path.expanduser('~/.osmosisd/'))
    subprocess.run(["wget -c "+proc.stdout.strip()+" -O - | lz4 -d | tar -xvf -"], shell=True)
    cosmovisorInit()
 


def mainNetLocation ():
    global location
    subprocess.run(["clear"], shell=True)
    print(bcolors.OKGREEN + """Please choose the location nearest to your node:
1) Netherlands
2) Singapore
3) SanFrancisco
    """)
    nodeLocationAns = input(bcolors.OKGREEN + 'Enter Choice: ')
    if nodeLocationAns == "1":
        location = "Netherlands"
        snapshotInstall()
    elif nodeLocationAns == "2":
        location = "Singapore"
        snapshotInstall()
    elif nodeLocationAns == "3":
        location = "SanFrancisco"
        snapshotInstall()      
    else:
        print ("Wrong selection, try again")
        mainNetLocation()

def mainNetType ():
    global fileName
    global location
    subprocess.run(["clear"], shell=True)
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned
2) Default
3) Archive
    """)

    nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ')
    if nodeTypeAns == "1":
        fileName = "osmosis-1-pruned"
        mainNetLocation()
    elif nodeTypeAns == "2":
        fileName = "osmosis-1-default"
        mainNetLocation()
    elif nodeTypeAns == "2":
        fileName = "osmosis-1-archive"
        location = "Netherlands"
        snapshotInstall()       
    else:
        print ("Wrong selection, try again")
        mainNetType()


def dataSyncSelection ():
    subprocess.run(["clear"], shell=True)
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) I have my own Osmosis snapshot, skip to setting up daemon 
    """) 
    dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ')
    if dataTypeAns == "1":
        mainNetType()
    elif dataTypeAns == "2":
        cosmovisorInit()       
    else:
        print ("Wrong selection, try again")
        dataSyncSelection()

def initSetup ():
    print(bcolors.OKGREEN + "Updating Packages" + bcolors.ENDC)
    subprocess.run(["sudo apt-get update && sudo apt-get upgrade -y"], shell=True)
    print(bcolors.OKGREEN + "Installing Make and GCC" + bcolors.ENDC)
    subprocess.run(["sudo apt install git build-essential ufw curl jq snapd --yes"], shell=True)
    print(bcolors.OKGREEN + "Installing Go" + bcolors.ENDC)
    subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --version 1.17.2"], shell=True)
    print(bcolors.OKGREEN + "Reloading Profile" + bcolors.ENDC)    
    subprocess.run([". ~/.profile"], shell=True)
    print(bcolors.OKGREEN + "Installing Osmosis V6 Binary" + bcolors.ENDC) 
    os.chdir(os.path.expanduser('~'))
    subprocess.run(["git clone https://github.com/osmosis-labs/osmosis"], shell=True)
    os.chdir(os.path.expanduser('~/osmosis'))
    subprocess.run(["git checkout v6.0.0 && make install"], shell=True)
    subprocess.run(["clear"], shell=True)
    nodeName= input(bcolors.OKGREEN + "Input desired node name (no quotes): ")
    print(bcolors.OKGREEN + "Initializing Osmosis Node " + nodeName + bcolors.ENDC)
    subprocess.run(["osmosisd","init", nodeName, "-o"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis" + bcolors.ENDC)
    subprocess.run(["wget -O ~/.osmosisd/config/genesis.json https://github.com/osmosis-labs/networks/raw/main/osmosis-1/genesis.json"], shell=True)
    dataSyncSelection()

def testing ():
    HOME = subprocess.run(["echo $HOME"], capture_output=True, shell=True, text=True)
    print(HOME.stdout)


def start ():
    subprocess.run(["clear"], shell=True)
    print(bcolors.OKGREEN + """
██████╗ ███████╗███╗   ███╗ ██████╗ ███████╗██╗███████╗
██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔════╝██║██╔════╝
██║   ██║███████╗██╔████╔██║██║   ██║███████╗██║███████╗
██║   ██║╚════██║██║╚██╔╝██║██║   ██║╚════██║██║╚════██║
╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝███████║██║███████║
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝                          


Welcome to the Osmosis node installer!
For more information, please visit docs.osmosis.zone

Please choose a network to join:
1) Mainnet (osmosis-1)
2) Testnet (osmosis-testnet-0)
    """)


    networkAns = input(bcolors.OKGREEN + 'Enter Choice: ')

    if networkAns == '1':
        initSetup()
    elif networkAns == '2':
        print("Testnet Setup")
    elif networkAns == '3':
        print("shortcut")
        cosmovisorInit()
    elif networkAns == '4':
        testing()
    else:
        print("Please only enter the number preceding the option and nothing else, in this case 1 or 2")
        start()


start()