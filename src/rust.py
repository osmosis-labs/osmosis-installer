import subprocess
import os
import globals
from style import bcolors
from init_setup import brachSelection
from style import colorprint


def installRust():
    isRustInstalled = subprocess.run(
        ["rustc --version"], capture_output=True, shell=True, text=True).stderr.strip()
    if "not found" not in isRustInstalled:
        return
    print(bcolors.OKGREEN + """Rust not found on your device. Do you want to install Rust?:
1) Yes, install Rust
2) No, do not install Rust
    """ + bcolors.ENDC)

    installRust = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if installRust == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(
            ["curl https://sh.rustup.rs -sSf | sh -s -- -y"], shell=True)
    elif installRust == "2":
        subprocess.run(["clear"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)
        installRust()


def setupContactEnvironment():
    globals.selected_my_env = os.environ.copy()
    globals.selected_my_env["PATH"] = "/"+globals.HOME+"/go/bin:/"+globals.HOME+"/go/bin:/" + \
        globals.HOME+"/.go/bin:"+globals.HOME + \
        "/.cargo/bin:" + globals.selected_my_env["PATH"]
    print(bcolors.OKGREEN + """Do you want to set up a basic contract environment?:
1) Yes, setup a basic contract environment
2) No, continue with the rest of the setup
    """ + bcolors.ENDC)

    setupContractEnv = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if setupContractEnv == "1":
        subprocess.run(["clear"], shell=True)
        colorprint("Setting 'stable' as the default release channel:")
        subprocess.run(["rustup default stable"], shell=True,
                       env=globals.selected_my_env)
        colorprint("Adding WASM as the compilation target:")
        subprocess.run(
            ["rustup target add wasm32-unknown-unknown"], shell=True, env=globals.selected_my_env)
        colorprint("Installing packages to generate the contract:")
        subprocess.run(
            ["cargo install cargo-generate --features vendored-openssl"], shell=True, env=globals.selected_my_env)
        subprocess.run(["cargo install cargo-run-script"],
                       shell=True, env=globals.selected_my_env)
        colorprint("Installing beaker:")
        subprocess.run(["cargo install -f beaker"],
                       shell=True, env=globals.selected_my_env)
    elif setupContractEnv == "2":
        subprocess.run(["clear"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)
        setupContactEnvironment()
