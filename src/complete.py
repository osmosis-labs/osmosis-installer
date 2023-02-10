from style import colorprint, bcolors


def partComplete():
    print(bcolors.OKGREEN +
          "Congratulations! You have successfully completed setting up the Osmosis daemon!")
    print(bcolors.OKGREEN +
          "The osmosisd service is NOT running in the background, and your data directory is empty")
    print(bcolors.OKGREEN + "If you intend to use osmosisd without syncing, you must include the '--node' flag after cli commands with the address of a public RPC node" + bcolors.ENDC)
    quit()


def clientComplete():
    print(bcolors.OKGREEN +
          "Congratulations! You have successfully completed setting up an Osmosis client node!")
    colorprint(
        "DO NOT start the osmosis daemon. You can query directly from the command line without starting the daemon!")
    quit()


def localOsmosisComplete():
    print(bcolors.OKGREEN +
          "Congratulations! You have successfully completed setting up a LocalOsmosis node!")
    print(bcolors.OKGREEN + "To start the local network:")
    print(bcolors.OKGREEN + "Ensure docker is running in the background if on linux or start the Docker application if on Mac")
    print(bcolors.OKGREEN + "Run 'cd $HOME/osmosis'")
    print(bcolors.OKGREEN +
          "First, you MUST clean your env, run 'make localnet-clean' and select 'yes'")
    print(bcolors.OKGREEN + "To start the node, run 'make localnet-start'")
    print(bcolors.OKGREEN +
          "Run 'osmosisd status' to check that you are now creating blocks")
    print(bcolors.OKGREEN + "To stop the node and retain data, run 'make localnet-stop'")
    print(bcolors.OKGREEN +
          "To stop the node and remove data, run 'make localnet-remove'")
    print(bcolors.OKGREEN + "To run LocalOsmosis on a different version, git checkout the desired branch, run 'make localnet-build', then follow the above instructions")
    print(bcolors.OKGREEN + "For more in depth information, see https://github.com/osmosis-labs/osmosis/blob/main/tests/localosmosis/README.md" + bcolors.ENDC)
    quit()


def complete():
    print(bcolors.OKGREEN +
          "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The osmosisd service is NOT running in the background")
    print(bcolors.OKGREEN +
          "You can start osmosisd with the following command: 'osmosisd start'" + bcolors.ENDC)
    quit()


def completeCosmovisor():
    print(bcolors.OKGREEN +
          "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN +
          "The cosmovisor service is currently running in the background")
    print(bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: 'sudo systemctl status cosmovisor'")
    colorprint(
        "To see the live logs from cosmovisor, run the following command: 'journalctl -u cosmovisor -f'")
    quit()


def completeOsmosisd():
    print(bcolors.OKGREEN +
          "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN +
          "The osmosisd service is currently running in the background")
    print(bcolors.OKGREEN + "To see the status of the osmosis daemon, run the following command: 'sudo systemctl status osmosisd'")
    colorprint(
        "To see the live logs from the osmosis daemon, run the following command: 'journalctl -u osmosisd -f'")
    quit()


def replayComplete():
    print(bcolors.OKGREEN +
          "Congratulations! You are currently replaying from genesis in a background service!")
    print(bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: 'sudo systemctl status cosmovisor'")
    colorprint(
        "To see the live logs from cosmovisor, run the following command: 'journalctl -u cosmovisor -f'")
    quit()


def replayDelay():
    print(bcolors.OKGREEN +
          "Congratulations! Osmosis is ready to replay from genesis on your command!")
    print(bcolors.OKGREEN +
          "YOU MUST MANUALLY INCREASE ULIMIT FILE SIZE BEFORE STARTING WITH `ulimit -n 200000`")
    print(bcolors.OKGREEN +
          "Use the command `cosmovisor start` to start the replay from genesis process")
    print(bcolors.OKGREEN +
          "It is recommended to run this in a tmux session if not running as a background service")
    print(bcolors.OKGREEN + "You must use `cosmovisor start` and not `osmosisd start` in order to upgrade automatically" + bcolors.ENDC)
    quit()
