import subprocess
import globals
import os
from style import bcolors, colorprint
from cosmovisor import cosmovisorService
from complete import replayComplete, replayDelay


def startReplayNow(args):
    print(bcolors.OKGREEN + """Do you want to start cosmovisor as a background service?
1) Yes, start cosmovisor as a background service and begin replay
2) No, exit and start on my own (will still auto update at upgrade heights)
    """ + bcolors.ENDC)
    if args.startReplay == True:
        startNow = '1'
    elif args.startReplay == False:
        startNow = '2'
    else:
        startNow = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if startNow == "1":
        subprocess.run(["clear"], shell=True)
        cosmovisorService()
        subprocess.run(["sudo systemctl start cosmovisor"],
                       shell=True, env=globals.selected_my_env)
        replayComplete()
    if startNow == "2":
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
        subprocess.run(["clear"], shell=True)
        replayDelay()
    else:
        subprocess.run(["clear"], shell=True)
        startReplayNow()


def replayFromGenesisLevelDb(args):
    colorprint("Setting Up Cosmovisor...")
    os.chdir(os.path.expanduser(globals.globals.HOME))
    subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["mkdir -p "+globals.osmo_home+"/cosmovisor"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(["mkdir -p "+globals.osmo_home+"/cosmovisor/genesis"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v4/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v5/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v7/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v9/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v11/bin"], shell=True, env=globals.selected_my_env)
    os.chdir(os.path.expanduser(globals.HOME+"/osmosis"))
    colorprint("Preparing v4 Upgrade...")
    subprocess.run(["git checkout v4.2.0"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v4/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v5/v6 Upgrade...")
    subprocess.run(["git checkout v6.4.1"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v5/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v7/v8 Upgrade...")
    subprocess.run(["git checkout v8.0.0"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v7/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v9/v10 Upgrade...")
    subprocess.run(["git checkout v10.0.1"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v9/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v11 Upgrade...")
    subprocess.run(["git checkout {v}".format(v=globals.NetworkVersion.MAINNET)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v11/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["git checkout v3.1.0"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["make install"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp " + globals.GOPATH + "/bin/osmosisd "+globals.osmo_home +
                   "/cosmovisor/genesis/bin"], shell=True, env=globals.selected_my_env)
    colorprint("Adding Persistent Peers For Replay...")
    peers = "b5ace00790c9cc7990370d7a117ef2a29f19b961@65.109.20.216:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.66.52.160:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.82.89.95:26656"
    subprocess.run(["sed -i -E 's/persistent_peers = \"\"/persistent_peers = \"" +
                   peers+"\"/g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["clear"], shell=True)
    startReplayNow(args)


def replayFromGenesisRocksDb(args):
    colorprint("Changing db_backend to rocksdb...")
    subprocess.run(["sed -i -E 's/db_backend = \"goleveldb\"/db_backend = \"rocksdb\"/g' "+globals.osmo_home +
                   "/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    colorprint("Installing rocksdb...")
    colorprint("This process may take 15 minutes or more")
    os.chdir(os.path.expanduser(globals.HOME))
    subprocess.run(["sudo apt-get install -y libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["git clone https://github.com/facebook/rocksdb.git"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    os.chdir(os.path.expanduser(globals.HOME+"/rocksdb"))
    subprocess.run(["git checkout v6.29.3"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["export CXXFLAGS='-Wno-error=deprecated-copy -Wno-error=pessimizing-move -Wno-error=class-memaccess'"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo make shared_lib"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo make install-shared INSTALL_PATH=/usr"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo echo 'export LD_LIBRARY_PATH=/usr/local/lib' >> $globals.HOME/.bashrc"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    globals.selected_my_env["LD_LIBRARY_PATH"] = "/usr/local/lib"
    colorprint("Setting Up Cosmovisor...")
    os.chdir(os.path.expanduser(globals.HOME))
    subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["mkdir -p "+globals.osmo_home+"/cosmovisor"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(["mkdir -p "+globals.osmo_home+"/cosmovisor/genesis"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v4/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v5/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v7/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v9/bin"], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["mkdir -p "+globals.osmo_home+"/cosmovisor/upgrades/v11/bin"], shell=True, env=globals.selected_my_env)
    os.chdir(os.path.expanduser(globals.HOME+"/osmosis"))
    colorprint("Preparing v4 Upgrade...")
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["git checkout v4.2.0"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["sed '/gorocksdb.*/d' ./go.mod"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["echo \" \" >> ./go.mod"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'replace github.com/tecbot/gorocksdb => github.com/cosmos/gorocksdb v1.2.0' >> ./go.mod"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["go mod tidy"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v4/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v5/v6 Upgrade...")
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["git checkout v6.4.1"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v5/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v7/v8 Upgrade...")
    subprocess.run(["git checkout v8.0.0"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v7/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v9/v10 Upgrade...")
    subprocess.run(["git checkout v10.0.1"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v9/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Preparing v11 Upgrade...")
    subprocess.run(["git checkout {v}".format(v=globals.NetworkVersion.MAINNET)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/upgrades/v11/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["git checkout v3.1.0"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["sed '/gorocksdb.*/d' ./go.mod"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["echo \" \" >> ./go.mod"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'require github.com/tecbot/gorocksdb v0.0.0-20191217155057-f0fad39f321c // indirect' >> ./go.mod"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["echo 'replace github.com/tecbot/gorocksdb => github.com/cosmos/gorocksdb v1.2.0' >> ./go.mod"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["go mod tidy"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["cp build/osmosisd "+globals.osmo_home+"/cosmovisor/genesis/bin"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make install"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["sudo /sbin/ldconfig -v"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Adding Persistent Peers For Replay...")
    peers = "b5ace00790c9cc7990370d7a117ef2a29f19b961@65.109.20.216:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.66.52.160:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.82.89.95:26656"
    subprocess.run(["sed -i -E 's/persistent_peers = \"\"/persistent_peers = \"" +
                   peers+"\"/g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["clear"], shell=True)
    startReplayNow(args)


def replayFromGenesisDb(args):
    print(bcolors.OKGREEN + """Please choose which database you want to use:
1) goleveldb (Default)
2) rocksdb (faster but less support)
    """ + bcolors.ENDC)
    if args.replayDbBackend == "goleveldb":
        databaseType = '1'
    elif args.replayDbBackend == "rocksdb":
        databaseType = '2'
    else:
        databaseType = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if databaseType == "1":
        subprocess.run(["clear"], shell=True)
        replayFromGenesisLevelDb(args)
    elif databaseType == "2":
        subprocess.run(["clear"], shell=True)
        replayFromGenesisRocksDb(args)
    else:
        subprocess.run(["clear"], shell=True)
        replayFromGenesisDb(args)
