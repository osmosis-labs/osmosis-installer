import os
import sys
import argparse
import subprocess
import platform
import configparser
from time import time, sleep
from enum import Enum

# CLI arguments
parser = argparse.ArgumentParser(description="Osmosis Installer")

DEFAULT_OSMOSIS_HOME = os.path.expanduser("~/.osmosisd")
DEFAULT_MONIKER = "osmosis"
NETWORK_CHOICES = ['osmosis-1', 'osmo-test-5']

parser.add_argument(
    "--home",
    type=str,
    help=f"Osmosis installation location",
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
    def __init__(self, chain_id, version, genesis_url, binary_url, seeds, rpc_node, addrbook_url, snapshot_url):
        self.chain_id = chain_id
        self.version = version
        self.genesis_url = genesis_url
        self.binary_url = binary_url
        self.seeds = seeds
        self.rpc_node = rpc_node
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
    rpc_node = "https://rpc.osmotest5.osmosis.zone:443",
    addrbook_url = "https://addrbook.osmotest5.osmosis.zone",
    snapshot_url = "https://snapshots.osmotest5.osmosis.zone/latest"
)

MAINNET = Network(
    chain_id = "osmosis-1",
    version = "v15.1.2",
    genesis_url = "https://osmosis.fra1.digitaloceanspaces.com/osmosis-1/genesis.json",
    binary_url = {
        "linux": {
            "amd64": "https://github.com/osmosis-labs/osmosis/releases/download/v15.1.2/osmosisd-15.1.2-linux-amd64",
            "arm64": "https://github.com/osmosis-labs/osmosis/releases/download/v15.1.2/osmosisd-15.1.2-linux-arm64",
        }
    },
    seeds = [
    ],
    rpc_node = "https://rpc.osmosis.zone:443",
    addrbook_url = "",
    snapshot_url = ""
)

# Terminal utils
class bcolors:
    OKGREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def clear_screen():
    os.system('clear')

# Messages

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
""" + bcolors.ENDC)


def client_complete_message():
    print(bcolors.OKGREEN + """
✨ Congratulations! You have successfully completed setting up an Osmosis client node! ✨
""" + bcolors.ENDC)

    print("🧪 Try running: " + bcolors.OKGREEN + "osmosisd status" + bcolors.ENDC)
    print()


# Options

def select_setup():

    print(bcolors.OKGREEN + """
Please choose a node type:

1) Full Node (downloads chain data and runs locally)
2) Client Node (sets up a daemon to query a public RPC)
3) LocalOsmosis Node (sets up a daemon to query a local Osmosis development RPC)
""" + bcolors.ENDC)

    while True:
        user_input = input("Enter your choice, or 'exit' to quit: ").strip()

        if user_input.lower() == "exit":
            print("Exiting the program...")
            sys.exit(0)

        if user_input not in ["1", "2", "3"]:
            print("Invalid input. Please choose a valid option.")
        else:
            break

    return user_input

def select_network():
    """
    Selects a network based on user input or command-line arguments.

    Returns:
        chosen_network (NetworkType): The chosen network, either MAINNET or TESTNET.

    Raises:
        SystemExit: If an invalid network is specified or the user chooses to exit the program.
    """

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
        print(bcolors.OKGREEN + f"""
Please choose a node type:

1) Mainnet ({MAINNET.chain_id})
2) Testnet ({TESTNET.chain_id})
""" + bcolors.ENDC)

        while True:
            chosen_network = input("Enter your choice, or 'exit' to quit: ").strip()

            if chosen_network.lower() == "exit":
                print("Exiting the program...")
                sys.exit(0)

            if chosen_network not in [NetworkType.MAINNET, NetworkType.TESTNET]:
                print("Invalid input. Please choose a valid option.")
            else:
                break
        
    if args.verbose:
        clear_screen()
        print(f"Chosen network: {NETWORK_CHOICES[int(chosen_network) - 1]}")

    return chosen_network


def download_binary(network):
    """
    Downloads the binary for the specified network based on the operating system and architecture.

    Args:
        network (NetworkType): The network type, either MAINNET or TESTNET.

    Raises:
        SystemExit: If the binary download URL is not available for the current operating system and architecture.

    """
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

    # TODO: Remove this
    operating_system = "linux"

    if operating_system in binary_urls and architecture in binary_urls[operating_system]:
        binary_url = binary_urls[operating_system][architecture]
    else:
        print(f"Binary download URL not available for {operating_system}/{architecture}")
        # TODO: Add option to build from source
        sys.exit(0)

    try:
        if args.verbose:
            print(f"Downloading binary from {binary_url}")

        osmosisd_path = "./osmosisd"  # Change the path as per your requirement

        subprocess.run(["wget", binary_url,"-q", "-O", osmosisd_path], check=True)
        os.chmod(osmosisd_path, 0o755)

        print("Binary downloaded successfully.")

    except subprocess.CalledProcessError:
        print("Failed to download the binary.")


def select_osmosis_home():
    """
    Selects the path for running the 'osmosisd init --home <SELECTED_HOME>' command.

    Returns:
        osmosis_home (str): The selected path.

    """
    if args.home:
        osmosis_home = args.home
    else:
        default_home = os.path.expanduser("~/.osmosisd")
        print(bcolors.OKGREEN + f"""
Do you want to install Osmosis in the default location?:

1) Yes, use default location {DEFAULT_OSMOSIS_HOME} (recommended)
2) No, specify custom location

💡 You can specify the location using the --home flag.
""" + bcolors.ENDC)

        while True:
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                osmosis_home = default_home
                break
            elif choice == "2":
                while True:
                    custom_home = input("Enter the path for Osmosis home: ").strip()
                    if custom_home != "":
                        osmosis_home = custom_home
                        break
                    else:
                        print("Invalid path. Please enter a valid directory.")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    return osmosis_home


def select_moniker():
    """
    Selects the moniker for the Osmosis node.

    Returns:
        moniker (str): The selected moniker.

    """
    if args.moniker:
        moniker = args.moniker
    else:
        print(bcolors.OKGREEN + f"""
Do you want to use the default moniker?

1) Yes, use default moniker ({DEFAULT_MONIKER})
2) No, specify custom moniker

💡 You can specify the moniker using the --moniker flag.
""" + bcolors.ENDC)

        while True:
            choice = input("Enter your choice: ")

            if choice == "1":
                moniker = DEFAULT_MONIKER
                break
            elif choice == "2":
                while True:
                    custom_moniker = input("Enter the custom moniker: ")
                    if custom_moniker.strip() != "":
                        moniker = custom_moniker
                        break
                    else:
                        print("Invalid moniker. Please enter a valid moniker.")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    return moniker


def initialize_home(osmosis_home, moniker):
    """
    Initializes the Osmosis home directory with the specified moniker.

    Args:
        osmosis_home (str): The chosen home directory.
        moniker (str): The moniker for the Osmosis node.

    """
    while True:
        print(bcolors.OKGREEN + f"""
Do you want to initialize the Osmosis home directory at '{osmosis_home}'?
""" + bcolors.ENDC)

        print(bcolors.RED + f"⚠️ All contents of the directory will be deleted." + bcolors.ENDC)

        print(bcolors.OKGREEN + f"""
1) Yes, proceed with initialization
2) No, quit
""" + bcolors.ENDC)
        
        choice = input("Enter your choice: ")

        if choice == "1":
            print(f"Initializing Osmosis home directory at '{osmosis_home}'...")
            try:
                subprocess.run(
                    ["rm", "-rf", osmosis_home], 
                    stderr=subprocess.DEVNULL, check=True)
                
                subprocess.run(
                    ["osmosisd", "init", moniker,  "-o", "--home", osmosis_home], 
                    stderr=subprocess.DEVNULL, check=True)
                print("Initialization completed successfully.")
                break
            except subprocess.CalledProcessError:
                print("Initialization failed.")
                print("Please check if the home directory is valid and has write permissions.")
                sys.exit(1)
        elif choice == "2":
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1 or 2.")


def customize_config(home, network):
    """
    Customizes the TOML configurations based on the network.

    Args:
        home (str): The home directory.
        network (str): The network identifier.

    """

    if network == NetworkType.TESTNET:
        client_toml = os.path.join(home, "config", "client.toml")

        with open(client_toml, "r") as config_file:
            lines = config_file.readlines()

        for i, line in enumerate(lines):
            if line.startswith("chain-id"):
                lines[i] = f'chain-id = "{TESTNET.chain_id}"\n'
            elif line.startswith("node"):
                lines[i] = f'node = "{TESTNET.rpc_node}"\n'

        with open(client_toml, "w") as config_file:
            config_file.writelines(lines)

        print("Configuration customized successfully.")
    else:
        print("No customization needed for the specified network.")


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
        clear_screen()
        # download_binary(chosen_network)
        clear_screen()
        chosen_home = select_osmosis_home()
        clear_screen()
        moniker = select_moniker()
        clear_screen()
        initialize_home(chosen_home, moniker)
        clear_screen()
        customize_config(chosen_home, chosen_network)
        clear_screen()
        client_complete_message()

    elif chosen_setup == SetupType.LOCALOSMOSIS:
        print("Setting up a LocalOsmosis node...")


main()
