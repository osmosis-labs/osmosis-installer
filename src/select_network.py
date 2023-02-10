import subprocess
import globals
from style import bcolors
from init_environment import initEnvironment
from init_setup import initSetup


def selectNetwork(args):
    print(bcolors.OKGREEN +
          """
Please choose a network to join:
1) Mainnet (osmosis-1)
2) Testnet (osmo-test-4)
    """ + bcolors.ENDC)

    if args.network == "osmosis-1":
        networkType = globals.NetworkType.MAINNET
    elif args.network == "osmo-test-4":
        networkType = globals.NetworkType.TESTNET
    else:
        networkType = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if networkType == globals.NetworkType.MAINNET and globals.selected_node == globals.NodeType.FULL:
        subprocess.run(["clear"], shell=True)
        globals.selected_version = globals.NetworkVersion.MAINNET
        initEnvironment(args)
    elif networkType == globals.NetworkType.MAINNET and globals.selected_node == globals.NodeType.CLIENT:
        subprocess.run(["clear"], shell=True)
        globals.selected_version = globals.NetworkVersion.MAINNET
        initSetup(args)
    elif networkType == globals.NetworkType.TESTNET and globals.selected_node == globals.NodeType.FULL:
        subprocess.run(["clear"], shell=True)
        globals.selected_version = globals.NetworkVersion.TESTNET
        initEnvironment(args)
    elif networkType == globals.NetworkType.TESTNET and globals.selected_node == globals.NodeType.CLIENT:
        subprocess.run(["clear"], shell=True)
        globals.selected_version = globals.NetworkVersion.TESTNET
        initSetup(args)
    else:
        subprocess.run(["clear"], shell=True)
        selectNetwork()
