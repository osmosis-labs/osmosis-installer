import os
import sys
import argparse
import shutil
import urllib.request
import platform
from time import time, sleep
from enum import Enum

# CLI arguments
parser = argparse.ArgumentParser(description="Osmosis Installer")

osmosisd_home = os.path.expanduser("~/.osmosisd")
NETWORK_CHOICES = ['osmosis-1', 'osmo-test-5']

parser.add_argument(
    "--home",
    type=str,
    default=osmosisd_home,
    help=f"Osmosis installation location\n(Default: '{osmosisd_home}')",
)

parser.add_argument(
    "--moniker",
    type=str,
    help="Moniker name for the node (Default: 'osmosis')",
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help="Enable verbose output",
    dest="verbose"
)

parser.add_argument(
    '-n',
    '--network',
    type=str,
    choices=NETWORK_CHOICES,
    help=f"Network to join: {NETWORK_CHOICES})",
)

# Choices
class SetupType(str, Enum):
    FULLNODE = "1"
    CLIENT = "2"
    LOCALOSMOSIS = "3"

class NetworkType(str, Enum):
    MAINNET = "1"
    TESTNET = "2"

# Network configurations
class Network:
    def __init__(self, chain_id, version, genesis_url, binary_url, seeds, addrbook_url, snapshot_url):
        self.chain_id = chain_id
        self.version = version
        self.genesis_url = genesis_url
        self.binary_url = binary_url
        self.seeds = seeds
        self.addrbook_url = addrbook_url
        self.snapshot_url = snapshot_url

    def display_info(self):
        print("Chain ID:", self.chain_id)
        print("Version:", self.version)
        print("Genesis URL:", self.genesis_url)
        print("Binary URLs:")
        for platform, urls in self.binary_url.items():
            print(f"  {platform}:")
            for arch, url in urls.items():
                print(f"    {arch}: {url}")
        print("Seeds:")
        for seed in self.seeds:
            print(f"  {seed}")
        print("Address Book:", self.addrbook_url)
        print("Snapshot URL:", self.snapshot_url)

TESTNET = Network(
    chain_id = "osmo-test-5",
    version = "v15.1.0-testnet",
    genesis_url = "https://osmosis.fra1.digitaloceanspaces.com/osmo-test-5/genesis.json",
    binary_url = {
        "linux": {
            "amd64": "https://osmosis.fra1.digitaloceanspaces.com/osmo-test-5/binaries/osmosisd-15.1.0-testnet-linux-amd64",
            "arm64": "https://osmosis.fra1.digitaloceanspaces.com/osmo-test-5/binaries/osmosisd-15.1.0-testnet-linux-arm64",
        }
    },
    seeds = [
        "a5f81c035ff4f985d5e7c940c7c3b846389b7374@167.235.115.14:26656",
        "05c41cc1fc7c8cb379e54d784bcd3b3907a1568e@157.245.26.231:26656",
        "7c2b9e76be5c2142c76b429d9c29e902599ceb44@157.245.21.183:26656",
        "f440c4980357d8b56db87ddd50f06bd551f1319a@5.78.98.19:26656",
        "ade4d8bc,8cbe014af6ebdf3cb7b1e9ad36f412c0@testnet-seeds.polkachu.com:12556",
    ],
    addrbook_url = "https://addrbook.osmotest5.osmosis.zone",
    snapshot_url = "https://snapshots.osmotest5.osmosis.zone/latest"
)

MAINNET = Network(
    chain_id = "osmosis-1",
    version = "v15.1.2",
    genesis_url = "https://osmosis.fra1.digitaloceanspaces.com/osmosis-1/genesis.json",
    binary_url = {
        "linux": {
            "amd64": "",
            "arm64": "4",
        }
    },
    seeds = [
    ],
    addrbook_url = "",
    snapshot_url = ""
)

# Terminal utils
class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

def clear_screen():
    os.system('clear')

# # Messages

def welcome_message():
    print(bcolors.OKGREEN + """
██████╗ ███████╗███╗   ███╗ ██████╗ ███████╗██╗███████╗
██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔════╝██║██╔════╝
██║   ██║███████╗██╔████╔██║██║   ██║███████╗██║███████╗
██║   ██║╚════██║██║╚██╔╝██║██║   ██║╚════██║██║╚════██║
╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝███████║██║███████║
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝

Welcome to the Osmosis node installer!

For more information, please visit docs.osmosis.zone
Ensure no osmosis services are running in the background

If you have an old Osmosis installation, 
it is recommended to back up any important Osmosis data before proceeding.
""" + bcolors.ENDC
)

def select_setup():

    print(bcolors.OKGREEN + """
Please choose a node type (1, 2, 3), or enter 'exit' to quit:

1) Full Node (downloads chain data and runs locally)
2) Client Node (sets up a daemon to query a public RPC)
3) LocalOsmosis Node (sets up a daemon to query a local Osmosis development RPC)
    """
    + bcolors.ENDC
)

    while True:
        user_input = input()

        if user_input.lower() == "exit":
            print("Exiting the program...")
            sys.exit(0)

        if user_input not in ["1", "2", "3"]:
            print("Invalid input. Please choose a valid option.")
        else:
            break

    return user_input


def select_network():

    # Check if network is specified in args
    if args.network:
        if args.network == MAINNET.chain_id:
            chosen_network = NetworkType.MAINNET
        elif args.network == TESTNET.chain_id:
            chosen_network = NetworkType.TESTNET
        else:
            print(f"Invalid network {args.network}. Please choose a valid network.")
            sys.exit(1)

    # If not, ask the user to choose a network
    else:
        print(bcolors.OKGREEN +
        f"""
Please choose a node type (1, 2), or enter 'exit' to quit:

1) Mainnet ({MAINNET.chain_id})
2) Testnet ({TESTNET.chain_id})
        """ + bcolors.ENDC)

        while True:
            chosen_network = input()

            if chosen_network.lower() == "exit":
                print("Exiting the program...")
                sys.exit(0)

            if chosen_network not in [NetworkType.MAINNET, NetworkType.TESTNET]:
                print("Invalid input. Please choose a valid option.")
            else:
                break
        
    if args.verbose:
        clear_screen()
        print(f"Chosen network: {NETWORK_CHOICES[int(chosen_network)]}")

    return chosen_network


def download_binary(network):

    operating_system = platform.system().lower()
    architecture = platform.machine()

    if architecture == "x86_64":
        architecture = "amd64"
    elif architecture == "aarch64":
        architecture = "arm64"

    if network == NetworkType.TESTNET:
        binary_urls = TESTNET.binary_url
    else:
        binary_urls = MAINNET.binary_url

    if operating_system in binary_urls and architecture in binary_urls[operating_system]:
        binary_url = binary_urls[operating_system][architecture]
    else:
        print(f"Binary download URL not available for {operating_system}/{architecture}")
        # TODO: Add option to build from source
        sys.exit(0)

    try:
        with urllib.request.urlopen(binary_url) as response:
            osmosisd_path = "./osmosisd"  # Change the path as per your requirement

            with open(osmosisd_path, 'wb') as file:
                shutil.copyfileobj(response, file)

            # Make the binary file executable
            os.chmod(osmosisd_path, 0o755)

        print("Binary downloaded successfully.")
    except urllib.error.URLError:
        print("Failed to download the binary.")


# Parse the command-line arguments
args = parser.parse_args()

def main():

    welcome_message()

    # Start the installation
    chosen_setup = select_setup()

    if chosen_setup == SetupType.FULLNODE:
        print("Setting up a full node...")

    elif chosen_setup == SetupType.CLIENT:
        print("Setting up a client node...")
        chosen_network = select_network()
        download_binary(chosen_network)

    elif chosen_setup == SetupType.LOCALOSMOSIS:
        print("Setting up a LocalOsmosis node...")

    clear_screen()
    print("Installation completed successfully!")

main()
