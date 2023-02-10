import subprocess
import globals
from style import bcolors
from init_setup import initSetup
from style import colorprint
from style import rlinput


def branchSelection(args):
    globals.selected_version = globals.NetworkVersion.LOCALOSMOSIS.value
    print(bcolors.OKGREEN + """
Would you like to run LocalOsmosis on the most recent release of Osmosis: {v} ?
1) Yes, use {v} (recommended)
2) No, I want to use a different version of Osmosis for LocalOsmosis from a branch on the osmosis repo
3) No, I want to use a different version of Osmosis for LocalOsmosis from a branch on an external repo
    """.format(
        v=globals.version) + bcolors.ENDC)

    branchSelect = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if branchSelect == "1":
        subprocess.run(["clear"], shell=True)
        initSetup(args)
    elif branchSelect == "2":
        subprocess.run(["clear"], shell=True)
        branchHandler(args)
    elif branchSelect == "3":
        subprocess.run(["clear"], shell=True)
        repoHandler(args)
    else:
        subprocess.run(["clear"], shell=True)
        branchSelection(args)


def branchHandler(args):
    colorprint("Input desired branch. Press enter for default branch")
    branch_def = subprocess.run(["echo {v}".format(
        v=globals.selected_version)], capture_output=True, shell=True, text=True).stdout.strip()

    globals.selected_version = rlinput(
        bcolors.OKGREEN + "Branch: " + bcolors.ENDC, branch_def)

    if globals.selected_version == "":
        print(bcolors.FAIL + "Please ensure your branch is not blank" + bcolors.FAIL)
        branchHandler(args)
    else:
        globals.selected_version = subprocess.run(
            ["echo "+globals.selected_version], capture_output=True, shell=True, text=True).stdout.strip()
        subprocess.run(["clear"], shell=True)
        initSetup(args)


def repoHandler(args):
    colorprint(
        "Input desired repo URL (do not include branch). Press enter for default location")
    repo_def = subprocess.run(
        ["echo "+globals.repo], capture_output=True, shell=True, text=True).stdout.strip()

    globals.repo = rlinput(
        bcolors.OKGREEN + "Repo URL: " + bcolors.ENDC, repo_def)

    if globals.repo.endswith("/"):
        print(bcolors.FAIL +
              "Please ensure your path does not end with `/`" + bcolors.FAIL)
        repoHandler(args)
    elif not globals.repo.startswith("https://"):
        print(bcolors.FAIL +
              "Please ensure your path begins with a `https://`" + bcolors.FAIL)
        repoHandler(args)
    elif globals.repo == "":
        print(bcolors.FAIL + "Please ensure your path is not blank" + bcolors.FAIL)
        repoHandler(args)
    else:
        globals.repo = subprocess.run(
            ["echo "+globals.repo], capture_output=True, shell=True, text=True).stdout.strip()
        subprocess.run(["clear"], shell=True)
        branchHandler(args)
