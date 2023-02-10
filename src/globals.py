import subprocess
import platform
from enum import Enum


class NetworkVersion(str, Enum):
    MAINNET = "v14.0.0"
    TESTNET = "v14.0.0"
    LOCALOSMOSIS = "v14.x"


class NetworkType(str, Enum):
    MAINNET = "1"
    TESTNET = "2"
    LOCALOSMOSIS = "3"


class NodeType(str, Enum):
    FULL = "1"
    CLIENT = "2"
    LOCALOSMOSIS = "3"


repo = "https://github.com/osmosis-labs/osmosis"
version = NetworkVersion.MAINNET
location = ""
fileName = ""
osmo_home = ""
node_name = ""

os_name = platform.system()
machine = platform.machine()

HOME = subprocess.run(
    ["echo $HOME"], capture_output=True, shell=True, text=True).stdout.strip()
USER = subprocess.run(
    ["echo $USER"], capture_output=True, shell=True, text=True).stdout.strip()
GOPATH = HOME+"/go"

selected_node = ""
selected_networktype = ""
selected_version = ""
selected_my_env = ""

# used in data_sync_selection.py
filename = ""
location = ""
