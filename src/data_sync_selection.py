import subprocess
import globals
from style import bcolors
from snapshots import snapshotInstall, infraSnapshotInstall
from complete import partComplete
from extra_swap import extraSwap
from location import mainNetLocation


def testNetType(args):
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned (recommended)
2) Archive
    """ + bcolors.ENDC)
    if args.snapshotTypeTestnet == "pruned":
        nodeTypeAns = "1"
    elif args.snapshotTypeTestnet == "archive":
        nodeTypeAns = "2"
    else:
        nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        globals.fileName = "osmotestnet-4-pruned"
        globals.location = "Netherlands"
        snapshotInstall(args)
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        globals.fileName = "osmotestnet-4-archive"
        globals.location = "Netherlands"
        snapshotInstall(args)
    else:
        subprocess.run(["clear"], shell=True)
        testNetType()


def mainNetType(args):
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned (recommended)
2) Default
3) Archive
    """ + bcolors.ENDC)
    if args.snapshotType == "pruned":
        nodeTypeAns = "1"
    elif args.snapshotType == "default":
        nodeTypeAns = "2"
    elif args.snapshotType == "archive":
        nodeTypeAns = "3"
    elif args.snapshotType == "infra":
        subprocess.run(["clear"], shell=True)
        infraSnapshotInstall(args)
    else:
        nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        globals.fileName = "osmosis-1-pruned"
        mainNetLocation(args)
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        globals.fileName = "osmosis-1-default"
        mainNetLocation(args)
    elif nodeTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        globals.fileName = "osmosis-1-archive"
        globals.location = "Netherlands"
        snapshotInstall(args)
    else:
        subprocess.run(["clear"], shell=True)
        mainNetType()


def dataSyncSelection(args):
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Start at block 1 and automatically upgrade at upgrade heights (replay from genesis, can also select rocksdb here)
3) Exit now, I only wanted to install the daemon
    """ + bcolors.ENDC)
    if args.dataSync == "snapshot":
        dataTypeAns = "1"
    elif args.dataSync == "genesis":
        dataTypeAns = "2"
    elif args.dataSync == "exit":
        dataTypeAns = "3"
    else:
        dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        mainNetType()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        extraSwap(args)
    # elif dataTypeAns == "2":
        #subprocess.run(["clear"], shell=True)
        #stateSyncInit ()
    elif dataTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        partComplete()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelection(args)


def dataSyncSelectionTest(args):
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Exit now, I only wanted to install the daemon
    """ + bcolors.ENDC)
    if args.dataSyncTestnet == "snapshot":
        dataTypeAns = "1"
    elif args.dataSyncTestnet == "exit":
        dataTypeAns = "2"
    else:
        dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        testNetType()
    # elif dataTypeAns == "2":
        #subprocess.run(["clear"], shell=True)
        # testnetStateSyncInit()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        partComplete()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest(args)
