import subprocess
import os
import globals
from style import bcolors
from style import colorprint
from style import rlinput
import rust


def installLocation(args):
    print(bcolors.OKGREEN + """Do you want to install Osmosis in the default location?:
1) Yes, use default location (recommended)
2) No, specify custom location
    """ + bcolors.ENDC)

    if args.installHome:
        locationChoice = '2'
    else:
        locationChoice = input(
            bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if locationChoice == "1":
        subprocess.run(["clear"], shell=True)
        globals.osmo_home = subprocess.run(
            ["echo $HOME/.osmosisd"], capture_output=True, shell=True, text=True).stdout.strip()
        initNodeName(args)
    elif locationChoice == "2":
        subprocess.run(["clear"], shell=True)
        installLocationHandler(args)
    else:
        subprocess.run(["clear"], shell=True)
        installLocation(args)


def installLocationHandler(args):
    colorprint(
        "Input desired installation location. Press enter for default location")
    location_def = subprocess.run(
        ["echo $HOME/.osmosisd"], capture_output=True, shell=True, text=True).stdout.strip()

    if args.installHome:
        globals.osmo_home = args.installHome
    else:
        globals.osmo_home = rlinput(
            bcolors.OKGREEN + "Installation Location: " + bcolors.ENDC, location_def)

    if globals.osmo_home.endswith("/"):
        print(bcolors.FAIL +
              "Please ensure your path does not end with `/`" + bcolors.FAIL)
        installLocationHandler(args)
    elif not globals.osmo_home.startswith("/") and not globals.osmo_home.startswith("$"):
        print(bcolors.FAIL + "Please ensure your path begin with a `/`" + bcolors.FAIL)
        installLocationHandler(args)
    elif globals.osmo_home == "":
        print(bcolors.FAIL + "Please ensure your path is not blank" + bcolors.FAIL)
        installLocationHandler(args)
    else:
        globals.osmo_home = subprocess.run(
            ["echo "+globals.osmo_home], capture_output=True, shell=True, text=True).stdout.strip()
        subprocess.run(["clear"], shell=True)
        initNodeName(args)


def initNodeName(args):
    colorprint(
        "AFTER INPUTTING NODE NAME, ALL PREVIOUS OSMOSIS DATA WILL BE RESET")

    if args.nodeName:
        globals.node_name = args.nodeName
    else:
        globals.node_name = input(
            bcolors.OKGREEN + "Input desired node name (no quotes, cant be blank): " + bcolors.ENDC)

    if globals.node_name and globals.selected_networktype == globals.NetworkType.MAINNET and globals.selected_node == globals.NodeType.FULL:
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r "+globals.osmo_home], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["rm -r "+globals.HOME+"/.osmosisd"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        # setupMainnet()

    elif globals.node_name and globals.selected_networktype == globals.NetworkType.TESTNET and globals.selected_node == globals.NodeType.FULL:
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r "+globals.osmo_home], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["rm -r "+globals.HOME+"/.osmosisd"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        # setupTestnet()
    elif globals.node_name and globals.selected_node == globals.NodeType.CLIENT or globals.selected_node == globals.NodeType.LOCALOSMOSIS:
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r "+globals.osmo_home], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        subprocess.run(["rm -r "+globals.HOME+"/.osmosisd"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)
        # clientSettings()
    else:
        subprocess.run(["clear"], shell=True)
        colorprint("Please insert a non-blank node name")
        initNodeName(args)
