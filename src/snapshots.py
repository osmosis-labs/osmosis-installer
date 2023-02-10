import subprocess
import os
import globals
from style import colorprint, rlinput
from complete import complete
from cosmovisor import cosmovisorInit


def infraSnapshotInstall(args):
    colorprint("Downloading Decompression Packages...")
    if globals.os_name == "Linux":
        subprocess.run(["sudo apt-get install wget liblz4-tool aria2 -y"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    else:
        subprocess.run(["brew install aria2"], shell=True,
                       env=globals.selected_my_env)
        subprocess.run(["brew install lz4"], shell=True,
                       env=globals.selected_my_env)
    colorprint("Downloading Snapshot...")
    proc = subprocess.run(["curl https://osmosis-snapshot.sfo3.cdn.digitaloceanspaces.com/osmosis.json|jq -r '.[] |select(.file==\"osmosis-1-pruned\")|.url'"],
                          capture_output=True, shell=True, text=True)
    os.chdir(os.path.expanduser(globals.osmo_home))
    subprocess.run(["wget -O - "+proc.stdout.strip() +
                   " | lz4 -d | tar -xvf -"], shell=True, env=globals.selected_my_env)
    subprocess.run(["clear"], shell=True)
    if globals.os_name == "Linux":
        cosmovisorInit(args)
    else:
        complete()


def snapshotInstall(args):
    colorprint("Downloading Decompression Packages...")
    if globals.os_name == "Linux":
        subprocess.run(["sudo apt-get install wget liblz4-tool aria2 -y"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    else:
        subprocess.run(["brew install aria2"], shell=True,
                       env=globals.selected_my_env)
        subprocess.run(["brew install lz4"], shell=True,
                       env=globals.selected_my_env)
    colorprint("Downloading Snapshot from " + globals.location + " ...")
    proc = subprocess.run(["curl -L https://quicksync.io/osmosis.json|jq -r '.[] |select(.file==\"" + globals.fileName +
                          "\")|select (.mirror==\"" + globals.location + "\")|.url'"], capture_output=True, shell=True, text=True)
    os.chdir(os.path.expanduser(globals.osmo_home))
    subprocess.run(["wget -O - "+proc.stdout.strip() +
                   " | lz4 -d | tar -xvf -"], shell=True, env=globals.selected_my_env)
    subprocess.run(["clear"], shell=True)
    if globals.os_name == "Linux":
        cosmovisorInit(args)
    else:
        complete()
