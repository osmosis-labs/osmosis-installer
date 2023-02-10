import subprocess
import os
from style import bcolors
import random
import globals
from style import colorprint, rlinput
from data_sync_selection import dataSyncSelection, dataSyncSelectionTest
from complete import partComplete, clientComplete, localOsmosisComplete


def setupLocalnet():
    global version
    print(bcolors.OKGREEN + "Initializing LocalOsmosis " +
          globals.node_name + bcolors.ENDC)
    os.chdir(os.path.expanduser(globals.HOME+"/osmosis"))
    print(bcolors.OKGREEN +
          "Building LocalOsmosis docker image {v}...".format(v=version) + bcolors.ENDC)
    subprocess.run(["make localnet-build"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["clear"], shell=True)
    localOsmosisComplete()


def setupMainnet(args):
    print(bcolors.OKGREEN + "Initializing Osmosis Node " +
          globals.node_name + bcolors.ENDC)
    #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+globals.osmo_home+"/config/app.toml"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["rm "+globals.osmo_home+"/config/config.toml"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["rm "+globals.osmo_home+"/config/addrbook.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["osmosisd init " + globals.node_name + " --chain-id=osmo-1 -o --home "+globals.osmo_home],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Downloading and Replacing Genesis...")
    subprocess.run(["wget -O "+globals.osmo_home+"/config/genesis.json https://github.com/osmosis-labs/networks/raw/main/osmosis-1/genesis.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Downloading and Replacing Addressbook...")
    subprocess.run(["wget -O "+globals.osmo_home+"/config/addrbook.json https://quicksync.io/addrbook.osmosis.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["clear"], shell=True)
    customPortSelection(args)


def setupTestnet(args):
    print(bcolors.OKGREEN + "Initializing Osmosis Node " +
          globals.node_name + bcolors.ENDC)
    #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+globals.osmo_home+"/config/config.toml"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["rm "+globals.osmo_home+"/config/app.toml"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["rm "+globals.osmo_home+"/config/addrbook.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["osmosisd init " + globals.node_name + " --chain-id=osmo-test-4 -o --home "+globals.osmo_home],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Downloading and Replacing Genesis...")
    subprocess.run(["wget -O "+globals.osmo_home+"/config/genesis.tar.bz2 wget https://github.com/osmosis-labs/networks/raw/main/osmo-test-4/genesis.tar.bz2"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    colorprint("Finding and Replacing Seeds...")
    peers = "4ab030b7fd75ed895c48bcc899b99c17a396736b@137.184.190.127:26656,3dbffa30baab16cc8597df02945dcee0aa0a4581@143.198.139.33:26656"
    subprocess.run(["sed -i -E 's/persistent_peers = \"\"/persistent_peers = \"" +
                   peers+"\"/g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["tar -xjf "+globals.osmo_home+"/config/genesis.tar.bz2"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(
        ["rm "+globals.osmo_home+"/config/genesis.tar.bz2"], shell=True)
    subprocess.run(["sed -i -E 's/seeds = \"21d7539792ee2e0d650b199bf742c56ae0cf499e@162.55.132.230:2000,295b417f995073d09ff4c6c141bd138a7f7b5922@65.21.141.212:2000,ec4d3571bf709ab78df61716e47b5ac03d077a1a@65.108.43.26:2000,4cb8e1e089bdf44741b32638591944dc15b7cce3@65.108.73.18:2000,f515a8599b40f0e84dfad935ba414674ab11a668@osmosis.blockpane.com:26656,6bcdbcfd5d2c6ba58460f10dbcfde58278212833@osmosis.artifact-staking.io:26656\"/seeds = \"0f9a9c694c46bd28ad9ad6126e923993fc6c56b1@137.184.181.105:26656\"/g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    colorprint("Downloading and Replacing Addressbook...")
    subprocess.run(["wget -O "+globals.osmo_home+"/config/addrbook.json https://quicksync.io/addrbook.osmotestnet.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
    subprocess.run(["clear"], shell=True)
    customPortSelection(args)


def customPortSelection(args):
    print(bcolors.OKGREEN + """Do you want to run Osmosis on default ports?:
1) Yes, use default ports (recommended)
2) No, specify custom ports
    """ + bcolors.ENDC)
    if args.ports:
        api_server = args.ports[0]
        grpc_server = args.ports[1]
        grpc_web = args.ports[2]
        abci_app_addr = args.ports[3]
        rpc_laddr = args.ports[4]
        p2p_laddr = args.ports[5]
        pprof_laddr = args.ports[6]
    else:
        portChoice = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

        if portChoice == "1":
            subprocess.run(["clear"], shell=True)
            pruningSettings(args)
        elif portChoice == "2":
            subprocess.run(["clear"], shell=True)
            colorprint("Input desired values. Press enter for default values")
            # app.toml
            api_server_def = "tcp://0.0.0.0:1317"
            grpc_server_def = "0.0.0.0:9090"
            grpc_web_def = "0.0.0.0:9091"
            # config.toml
            abci_app_addr_def = "tcp://127.0.0.1:26658"
            rpc_laddr_def = "tcp://127.0.0.1:26657"
            p2p_laddr_def = "tcp://0.0.0.0:26656"
            pprof_laddr_def = "localhost:6060"
            # user input
            api_server = rlinput(
                bcolors.OKGREEN + "(1/7) API Server: " + bcolors.ENDC, api_server_def)
            grpc_server = rlinput(
                bcolors.OKGREEN + "(2/7) gRPC Server: " + bcolors.ENDC, grpc_server_def)
            grpc_web = rlinput(bcolors.OKGREEN +
                               "(3/7) gRPC Web: " + bcolors.ENDC, grpc_web_def)
            abci_app_addr = rlinput(
                bcolors.OKGREEN + "(4/7) ABCI Application Address: " + bcolors.ENDC, abci_app_addr_def)
            rpc_laddr = rlinput(
                bcolors.OKGREEN + "(5/7) RPC Listening Address: " + bcolors.ENDC, rpc_laddr_def)
            p2p_laddr = rlinput(
                bcolors.OKGREEN + "(6/7) P2P Listening Address: " + bcolors.ENDC, p2p_laddr_def)
            pprof_laddr = rlinput(
                bcolors.OKGREEN + "(7/7) pprof Listening Address: " + bcolors.ENDC, pprof_laddr_def)
        elif portChoice and portChoice != "1" or portChoice != "2":
            subprocess.run(["clear"], shell=True)
            customPortSelection()

    # change app.toml values
    subprocess.run(["sed -i -E 's|tcp://0.0.0.0:1317|"+api_server +
                   "|g' "+globals.osmo_home+"/config/app.toml"], shell=True)
    subprocess.run(["sed -i -E 's|0.0.0.0:9090|"+grpc_server +
                   "|g' "+globals.osmo_home+"/config/app.toml"], shell=True)
    subprocess.run(["sed -i -E 's|0.0.0.0:9091|"+grpc_web +
                   "|g' "+globals.osmo_home+"/config/app.toml"], shell=True)

    # change config.toml values
    subprocess.run(["sed -i -E 's|tcp://127.0.0.1:26658|"+abci_app_addr +
                   "|g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's|tcp://127.0.0.1:26657|"+rpc_laddr +
                   "|g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's|tcp://0.0.0.0:26656|"+p2p_laddr +
                   "|g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's|localhost:6060|"+pprof_laddr +
                   "|g' "+globals.osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["clear"], shell=True)

    pruningSettings(args)


def clientSettings():
    if globals.selected_networktype == globals.NetworkType.MAINNET:
        print(bcolors.OKGREEN + "Initializing Osmosis Client Node " +
              globals.node_name + bcolors.ENDC)
        #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm "+globals.osmo_home+"/config/client.toml"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["osmosisd init " + globals.node_name + " --chain-id=osmosis-1 -o --home "+globals.osmo_home],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        colorprint("Changing Client Settings...")
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"osmosis-1\"/g' " +
                       globals.osmo_home+"/config/client.toml"], shell=True)
        #subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://rpc-osmosis.blockapsis.com:443\"|g' "+osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"http://osmosis.artifact-staking.io:26657\"|g' " +
                       globals.osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()

    elif globals.selected_networktype == globals.NetworkType.TESTNET:
        print(bcolors.OKGREEN + "Initializing Osmosis Client Node " +
              globals.node_name + bcolors.ENDC)
        #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm "+globals.osmo_home+"/config/client.toml"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["osmosisd init " + globals.node_name + " --chain-id=osmo-test-4 -o --home "+globals.osmo_home],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        colorprint("Changing Client Settings...")
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"osmo-test-4\"/g' " +
                       globals.osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://rpc.testnet.osmosis.zone:443\"|g' " +
                       globals.osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()

    elif globals.selected_networktype == globals.NetworkType.LOCALOSMOSIS:
        print(bcolors.OKGREEN + "Initializing LocalOsmosis Node " +
              globals.node_name + bcolors.ENDC)
        subprocess.run(["rm "+globals.osmo_home+"/config/client.toml"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["osmosisd init " + globals.node_name + " --chain-id=localosmosis -o --home "+globals.osmo_home],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        colorprint("Changing Client Settings...")
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"localosmosis\"/g' " +
                       globals.osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"tcp://127.0.0.1:26657\"|g' " +
                       globals.osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        setupLocalnet()


def pruningSettings(args):
    print(bcolors.OKGREEN + """Please choose your desired pruning settings:
1) Default: (keep last 100,000 states to query the last week worth of data and prune at 100 block intervals)
2) Nothing: (keep everything, select this if running an archive node)
3) Everything: (modified prune everything due to bug, keep last 10,000 states and prune at a random prime block interval)
    """ + bcolors.ENDC)

    if args.pruning == "default":
        pruneAns = '1'
    elif args.pruning == "nothing":
        pruneAns = '2'
    elif args.pruning == "everything":
        pruneAns = '3'
    else:
        pruneAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if pruneAns == "1" and globals.selected_networktype == globals.NetworkType.MAINNET:
        subprocess.run(["clear"], shell=True)
        dataSyncSelection()
    elif pruneAns == "1" and globals.selected_networktype == globals.NetworkType.TESTNET:
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "2" and globals.selected_networktype == globals.NetworkType.MAINNET:
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' " +
                       globals.osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelection()
    elif pruneAns == "2" and globals.selected_networktype == globals.NetworkType.TESTNET:
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' " +
                        globals.osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "3" and globals.selected_networktype == globals.NetworkType.MAINNET:
        primeNum = random.choice([x for x in range(11, 97) if not [
                                 t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' " +
                        globals.osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' " +
                        globals.osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \"" +
                       str(primeNum)+"\"/g' " + globals.osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelection()
    elif pruneAns == "3" and globals.selected_networktype == globals.NetworkType.TESTNET:
        primeNum = random.choice([x for x in range(11, 97) if not [
                                 t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' " +
                        globals.osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' " +
                        globals.osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \"" +
                       str(primeNum)+"\"/g' " + globals.osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelectionTest()
    else:
        subprocess.run(["clear"], shell=True)
        pruningSettings(args)
