import subprocess
import os
import globals
from style import colorprint, bcolors
from complete import complete, completeOsmosisd, completeCosmovisor
from osmosisd import osmosisdService


def cosmovisorInit(args):
    print(bcolors.OKGREEN + """Do you want to use Cosmovisor to automate future upgrades?
1) Yes, install cosmovisor and set up background service
2) No, just set up an osmosisd background service (recommended)
3) Don't install cosmovisor and don't set up a background service
    """ + bcolors.ENDC)
    if args.cosmovisorService == "cosmoservice":
        useCosmovisor = '1'
    elif args.cosmovisorService == "osmoservice":
        useCosmovisor = '2'
    elif args.cosmovisorService == "noservice":
        useCosmovisor = '3'
    else:
        useCosmovisor = input(
            bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if useCosmovisor == "1":
        subprocess.run(["clear"], shell=True)
        colorprint("Setting Up Cosmovisor...")
        os.chdir(os.path.expanduser(globals.HOME))
        subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["mkdir -p "+globals.osmo_home+"/cosmovisor"],
                       shell=True, env=globals.selected_my_env)
        subprocess.run(
            ["mkdir -p "+globals.osmo_home+"/cosmovisor/genesis"], shell=True, env=globals.selected_my_env)
        subprocess.run(
            ["mkdir -p "+globals.osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=globals.selected_my_env)
        subprocess.run(
            ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades"], shell=True, env=globals.selected_my_env)
        subprocess.run(
            ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v9/bin"], shell=True, env=globals.selected_my_env)
        os.chdir(os.path.expanduser(globals.HOME+"/osmosis"))
        subprocess.run(["git checkout {v}".format(v=globals.NetworkVersion.MAINNET)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["make build"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v9/bin"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["cp " + globals.GOPATH + "/bin/osmosisd "+globals.osmo_home +
                       "/cosmovisor/genesis/bin"], shell=True, env=globals.selected_my_env)
        cosmovisorService()
        subprocess.run(["sudo systemctl start cosmovisor"],
                       shell=True, env=globals.selected_my_env)
        subprocess.run(["clear"], shell=True)
        completeCosmovisor()
    elif useCosmovisor == "2":
        osmosisdService()
        subprocess.run(["sudo systemctl start osmosisd"],
                       shell=True, env=globals.selected_my_env)
        subprocess.run(["clear"], shell=True)
        completeOsmosisd()
    elif useCosmovisor == "3":
        subprocess.run(["clear"], shell=True)
        complete()
    else:
        subprocess.run(["clear"], shell=True)
        cosmovisorInit(args)


def cosmovisorService():
    colorprint("Creating Cosmovisor Service")
    subprocess.run(["echo '# Setup Cosmovisor' >> "+globals.HOME +
                   "/.profile"], shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'export DAEMON_NAME=osmosisd' >> " +
                   globals.HOME+"/.profile"], shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'export DAEMON_HOME="+globals.osmo_home +
                   "' >> "+globals.HOME+"/.profile"], shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'export DAEMON_ALLOW_DOWNLOAD_BINARIES=false' >> " +
                   globals.HOME+"/.profile"], shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'export DAEMON_LOG_BUFFER_SIZE=512' >> " +
                   globals.HOME+"/.profile"], shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'export DAEMON_RESTART_AFTER_UPGRADE=true' >> " +
                   globals.HOME+"/.profile"], shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'export UNSAFE_SKIP_BACKUP=true' >> " +
                   globals.HOME+"/.profile"], shell=True, env=globals.selected_my_env)
    subprocess.run(["""echo '[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_HOME=""" + globals.osmo_home+"""\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
Environment=\"UNSAFE_SKIP_BACKUP=true\"
User =""" + globals.USER+"""
ExecStart="""+globals.HOME+"""/go/bin/cosmovisor start --home """+globals.osmo_home+"""
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
[Install]
WantedBy=multi-user.target
' >cosmovisor.service
    """], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["sudo mv cosmovisor.service /lib/systemd/system/cosmovisor.service"], shell=True, env=globals.selected_my_env)
    subprocess.run(["sudo systemctl daemon-reload"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(["systemctl restart systemd-journald"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(["clear"], shell=True)
