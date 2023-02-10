import subprocess
import os
import globals
from style import colorprint, bcolors
import rust
from install_location import installLocation


def initSetup(args):
    # calling import here to fix circular import.
    # performace cost is negligible because imports are cached and future imports will
    # refer to the cached copy.
    from handlers import branchSelection
    if globals.os_name == "Linux":
        colorprint("Please wait while the following processes run:")
        colorprint("(1/4) Updating Packages...")
        subprocess.run(["sudo apt-get update"],
                       stdout=subprocess.DEVNULL, shell=True)
        subprocess.run(["DEBIAN_FRONTEND=noninteractive apt-get -y upgrade"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        colorprint("(2/4) Installing make and GCC...")
        subprocess.run(["sudo apt install git build-essential ufw curl jq snapd --yes"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        colorprint("(3/4) Installing Go...")
        subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --remove"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --version 1.19"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        os.chdir(os.path.expanduser(globals.HOME))
        gitClone = subprocess.Popen(
            ["git clone "+globals.repo], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, shell=True)
        if "Repository not found" in gitClone.communicate()[1]:
            subprocess.run(["clear"], shell=True)
            print(bcolors.OKGREEN + globals.repo + """ repo provided by user does not exist, try another URL
            """ + bcolors.ENDC)
            branchSelection(args)
        os.chdir(os.path.expanduser(globals.HOME+"/osmosis"))
        subprocess.run(["git stash"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["git pull"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)

        print(bcolors.OKGREEN +
              "(4/4) Installing Osmosis {v} Binary...".format(v=globals.selected_version) + bcolors.ENDC)
        gitCheckout = subprocess.Popen(["git checkout {v}".format(
            v=globals.selected_version)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, shell=True)
        if "did not match any file(s) known to git" in gitCheckout.communicate()[1]:
            subprocess.run(["clear"], shell=True)
            print(bcolors.OKGREEN + globals.selected_version + """ branch provided by user does not exist, try another branch
            """ + bcolors.ENDC)
            branchSelection(args)

        globals.selected_my_env = os.environ.copy()
        globals.selected_my_env["PATH"] = "/"+globals.HOME+"/go/bin:/"+globals.HOME + \
            "/go/bin:/"+globals.HOME+"/.go/bin:" + \
            globals.selected_my_env["PATH"]
        subprocess.run(["make install"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=globals.selected_my_env)

        if globals.selected_node == globals.NodeType.LOCALOSMOSIS:
            subprocess.run(["clear"], shell=True)
            colorprint("Installing Docker...")
            subprocess.run(["sudo apt-get remove docker docker-engine docker.io"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo apt-get update"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo apt install docker.io -y"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            colorprint("Installing Docker-Compose...")
            subprocess.run(["sudo apt install docker-compose -y"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            colorprint("Adding Wallet Keys to Keyring...")
            subprocess.run(["make localnet-keys"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["clear"], shell=True)
            rust.installRust()
            print("INSTALL RUST")
            subprocess.run(["clear"], shell=True)
            rust.setupContactEnvironment()
            print("SETUP CONTACT ENV")
        subprocess.run(["clear"], shell=True)

    elif globals.os_name == "Darwin":
        colorprint("Please wait while the following processes run:")
        colorprint(
            "(1/4) Checking for brew and wget. If not present, installing...")
        subprocess.run(["sudo chown -R $(whoami) /usr/local/var/homebrew"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["echo | /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)\""],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' >> "+globals.HOME +
                       "/.zprofile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["eval \"$(/opt/homebrew/bin/brew shellenv)\""],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        globals.selected_my_env = os.environ.copy()
        globals.selected_my_env["PATH"] = "/opt/homebrew/bin:/opt/homebrew/bin/brew:" + \
            globals.selected_my_env["PATH"]
        subprocess.run(["brew install wget"], shell=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=globals.selected_my_env)
        colorprint("(2/4) Checking/installing jq...")
        subprocess.run(["brew install jq"], shell=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=globals.selected_my_env)
        colorprint("(3/4) Checking/installing Go...")
        subprocess.run(["brew install coreutils"], shell=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=globals.selected_my_env)
        subprocess.run(["asdf plugin-add golang https://github.com/kennyp/asdf-golang.git"],
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=globals.selected_my_env)
        subprocess.run(["asdf install golang 1.19"], shell=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=globals.selected_my_env)
        os.chdir(os.path.expanduser(globals.HOME))
        gitClone = subprocess.Popen(
            ["git clone "+globals.repo], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, shell=True)
        if "Repository not found" in gitClone.communicate()[1]:
            subprocess.run(["clear"], shell=True)
            print(bcolors.OKGREEN + globals.repo + """ repo provided by user does not exist, try another URL
            """ + bcolors.ENDC)
            branchSelection(args)
        os.chdir(os.path.expanduser(globals.HOME+"/osmosis"))
        subprocess.run(["git stash"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["git pull"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)

        print(bcolors.OKGREEN +
              "(4/4) Installing Osmosis {v} Binary...".format(v=globals.selected_version) + bcolors.ENDC)
        gitCheckout = subprocess.Popen(["git checkout {v}".format(
            v=globals.selected_version)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, shell=True)
        if "did not match any file(s) known to git" in gitCheckout.communicate()[1]:
            subprocess.run(["clear"], shell=True)
            print(bcolors.OKGREEN + globals.selected_version + """ branch provided by user does not exist, try another branch
            """ + bcolors.ENDC)
            branchSelection(args)

        globals.selected_my_env["PATH"] = "/"+globals.HOME+"/go/bin:/"+globals.HOME + \
            "/go/bin:/"+globals.HOME+"/.go/bin:" + \
            globals.selected_my_env["PATH"]
        subprocess.run(["make install"], shell=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=globals.selected_my_env)

        if globals.selected_node == globals.NodeType.LOCALOSMOSIS:
            subprocess.run(["clear"], shell=True)
            colorprint("Installing Docker...")
            subprocess.run(["brew install docker"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            colorprint("Installing Docker-Compose...")
            subprocess.run(["brew install docker-compose"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            colorprint("Adding Wallet Keys to Keyring...")
            subprocess.run(["make localnet-keys"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["clear"], shell=True)
            rust.installRust()
            print("INSTALL RUST")
            subprocess.run(["clear"], shell=True)
            rust.setupContactEnvironment()
            print("SETUP CONTACT ENV")
        subprocess.run(["clear"], shell=True)
    installLocation(args)
