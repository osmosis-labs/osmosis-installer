import subprocess
import argparse
import sys
import globals
from style import bcolors
import select_network
from init_setup import brachSelection

# os.remove(sys.argv[0])


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        return ', '.join(action.option_strings)

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def fmt(prog): return CustomHelpFormatter(prog, max_help_position=30)


osmo_home = subprocess.run(
    ["echo $HOME/.osmosisd"], capture_output=True, shell=True, text=True).stdout.strip()

parser = argparse.ArgumentParser(
    description="Osmosis Installer", formatter_class=fmt)
parser._optionals.title = 'Optional Arguments'

if not len(sys.argv) > 1:
    parser.set_defaults(mainnetDefault=False, testnetDefault=False, swapOn=None, installHome=None, nodeName=None, ports=None, nodeType=None, network=None, pruning=None, cosmovisorService=None,
                        dataSyncTestnet=None, snapshotTypeTestnet=None, dataSync=None, snapshotType=None, snapshotLocation=None, replayDbBackend=None, extraSwap=None, startReplay=None)

args = parser.parse_args()

if args.testnetDefault == True:
    args.network = 'osmo-test-4'


def start():
    subprocess.run(["clear"], shell=True)

    def restart():
        print(bcolors.OKGREEN + """
 ██████╗ ███████╗███╗   ███╗ ██████╗ ███████╗██╗███████╗
██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔════╝██║██╔════╝
██║   ██║███████╗██╔████╔██║██║   ██║███████╗██║███████╗
██║   ██║╚════██║██║╚██╔╝██║██║   ██║╚════██║██║╚════██║
╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝███████║██║███████║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝


Welcome to the Osmosis node installer!

Mainnet version: {m}
Testnet version: {t}

For more information, please visit docs.osmosis.zone
Ensure no osmosis services are running in the background
If running over an old osmosis installation, back up
any important osmosis data before proceeding

Please choose a node type:
1) Full Node (download chain data and run locally)
2) Client Node (setup a daemon and query a public RPC)
3) LocalOsmosis Node (setup a daemon and query a localOsmosis development RPC)
        """.format(
            m=globals.NetworkVersion.MAINNET.value,
            t=globals.NetworkVersion.TESTNET.value) + bcolors.ENDC)

        if args.nodeType == 'full':
            globals.selected_node = globals.NodeType.FULL
        elif args.nodeType == 'client':
            globals.selected_node = globals.NodeType.CLIENT
        elif args.nodeType == 'local':
            globals.selected_node = globals.NodeType.LOCALOSMOSIS
        else:
            globals.selected_node = input(
                bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

        if globals.selected_node == globals.NodeType.FULL:
            subprocess.run(["clear"], shell=True)
            select_network.selectNetwork(args)
        elif globals.selected_node == globals.NodeType.CLIENT:
            subprocess.run(["clear"], shell=True)
            select_network.selectNetwork(args)
        elif globals.selected_node == globals.NodeType.LOCALOSMOSIS:
            globals.selected_networktype = globals.NetworkType.LOCALOSMOSIS
            subprocess.run(["clear"], shell=True)
            brachSelection(args)
        else:
            subprocess.run(["clear"], shell=True)
            restart()
    restart()


start()
