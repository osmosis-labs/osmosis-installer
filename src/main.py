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


# automated commands ("auto" group)
auto = parser.add_argument_group('Automated')

auto.add_argument(
    '-m',
    '--mainnet-default',
    action='store_true',
    help='R|Use all default settings with no input for mainnet\n ',
    dest="mainnetDefault")

auto.add_argument(
    '-t',
    '--testnet-default',
    action='store_true',
    help='R|Use all default settings with no input for testnet\n ',
    dest="testnetDefault")

# mainnet and testnet commands ("both" group)
both = parser.add_argument_group('Mainnet and Testnet')

both.add_argument(
    '-s',
    '--swap',
    type=bool,
    default=True,
    help='R|Use swap if less than 32Gb RAM are detected \nDefault (bool): True\n ',
    dest="swapOn")

both.add_argument(
    '-i',
    '--install-home',
    type=str,
    default=osmo_home,
    help='R|Osmosis installation location \nDefault: "'+osmo_home+'"\n ',
    dest="installHome")

both.add_argument(
    '-na',
    '--name',
    type=str,
    default="defaultNode",
    help='R|Node name \nDefault: "defaultNode"\n ',
    dest="nodeName")

portDefault = 'tcp://0.0.0.0:1317;0.0.0.0:9090;0.0.0.0:9091;tcp://127.0.0.1:26658;tcp://127.0.0.1:26657;tcp://0.0.0.0:26656;localhost:6060'
both.add_argument(
    '-p',
    '--ports',
    type=lambda s: [str(item) for item in s.split(';')],
    default=portDefault,
    help='R|Single string separated by semicolons of ports. Order must be api, grpc server, grpc web, abci app addr, rpc laddr, p2p laddr, and pprof laddr \nDefault: \"'+portDefault+'\"\n ',
    dest="ports")

nodeTypeChoices = ['full', 'client', 'local']
both.add_argument(
    '-ty',
    '--type',
    type=str,
    choices=nodeTypeChoices,
    default='full',
    help='R|Node type \nDefault: "full" '+str(nodeTypeChoices)+'\n ',
    dest="nodeType")

networkChoices = ['osmosis-1', 'osmo-test-4']
both.add_argument(
    '-n',
    '--network',
    type=str,
    choices=networkChoices,
    default='osmosis-1',
    help='R|Network to join \nDefault: "osmosis-1" '+str(networkChoices)+'\n ',
    dest="network")

pruningChoices = ['default', 'nothing', 'everything']
both.add_argument(
    '-pr',
    '--prune',
    type=str,
    choices=pruningChoices,
    default='everything',
    help='R|Pruning settings \nDefault: "everything" ' +
    str(pruningChoices)+'\n ',
    dest="pruning")

cosmovisorServiceChoices = ['cosmoservice', 'osmoservice', 'noservice']
both.add_argument(
    '-cvs',
    '--cosmovisor-service',
    type=str,
    choices=cosmovisorServiceChoices,
    default='osmoservice',
    help='R|Start with cosmovisor systemctl service, osmosisd systemctl service, or exit without creating or starting a service \nDefault: "osmoservice" ' +
    str(cosmovisorServiceChoices),
    dest="cosmovisorService")

# testnet only commands ("testnet" group)
testnet = parser.add_argument_group('Testnet only')

dataSyncTestnetChoices = ['snapshot', 'exit']
testnet.add_argument(
    '-dst',
    '--data-sync-test',
    type=str,
    choices=dataSyncTestnetChoices,
    default='snapshot',
    help='R|Data sync options \nDefault: "snapshot" ' +
    str(dataSyncTestnetChoices)+'\n ',
    dest="dataSyncTestnet")

snapshotTypeTestnetChoices = ['pruned', 'archive']
testnet.add_argument(
    '-stt',
    '--snapshot-type-test',
    type=str,
    choices=snapshotTypeTestnetChoices,
    default='pruned',
    help='R|Snapshot type \nDefault: "pruned" ' +
    str(snapshotTypeTestnetChoices)+'\n ',
    dest="snapshotTypeTestnet")

# mainnet only commands ("mainnet" group)
mainnet = parser.add_argument_group('Mainnet only')

dataSyncTypeChoices = ['snapshot', 'genesis', 'exit']
mainnet.add_argument(
    '-ds',
    '--data-sync',
    type=str,
    choices=dataSyncTypeChoices,
    default='snapshot',
    help='R|Data sync options \nDefault: "snapshot" ' +
    str(dataSyncTypeChoices)+'\n ',
    dest="dataSync")

snapshotTypeChoices = ['pruned', 'default', 'archive', 'infra']
mainnet.add_argument(
    '-st',
    '--snapshot-type',
    type=str,
    choices=snapshotTypeChoices,
    default='pruned',
    help='R|Snapshot type \nDefault: "pruned" '+str(snapshotTypeChoices)+'\n ',
    dest="snapshotType")

snapshotLocationChoices = ['netherlands', 'singapore', 'sanfrancisco']
mainnet.add_argument(
    '-sl',
    '--snapshot-location',
    type=str,
    choices=snapshotLocationChoices,
    default='netherlands',
    help='R|Snapshot location \nDefault: "netherlands" ' +
    str(snapshotLocationChoices)+'\n ',
    dest="snapshotLocation")

replayDbBackendChoices = ['goleveldb', 'rocksdb']
mainnet.add_argument(
    '-rdb',
    '--replay-db-backend',
    type=str,
    choices=replayDbBackendChoices,
    default='goleveldb',
    help='R|Database backend when replaying from genesis\nDefault: "goleveldb" ' +
    str(replayDbBackendChoices)+'\n ',
    dest="replayDbBackend")

mainnet.add_argument(
    '-es',
    '--extra-swap',
    type=bool,
    default=True,
    help='R|Use extra swap if less than 64Gb RAM are detected when syncing from genesis\nDefault (bool): True\n ',
    dest="extraSwap")

mainnet.add_argument(
    '-sr',
    '--start-replay',
    type=bool,
    default=True,
    help='R|Immediately start replay on completion\nDefault (bool): True\n ',
    dest="startReplay")

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
