# import subprocess
# import globals
# from style import bcolors
# from init_setup import initSetup
# from style import colorprint
# from style import rlinput


# def branchHandler():
#     colorprint("Input desired branch. Press enter for default branch")
#     branch_def = subprocess.run(["echo {v}".format(
#         v=globals.selected_version)], capture_output=True, shell=True, text=True).stdout.strip()

#     globals.selected_version = rlinput(
#         bcolors.OKGREEN + "Branch: " + bcolors.ENDC, branch_def)

#     if globals.selected_version == "":
#         print(bcolors.FAIL + "Please ensure your branch is not blank" + bcolors.FAIL)
#         branchHandler()
#     else:
#         globals.selected_version = subprocess.run(
#             ["echo "+globals.selected_version], capture_output=True, shell=True, text=True).stdout.strip()
#         subprocess.run(["clear"], shell=True)
#         initSetup()


# def repoHandler():
#     colorprint(
#         "Input desired repo URL (do not include branch). Press enter for default location")
#     repo_def = subprocess.run(
#         ["echo "+globals.repo], capture_output=True, shell=True, text=True).stdout.strip()

#     globals.repo = rlinput(
#         bcolors.OKGREEN + "Repo URL: " + bcolors.ENDC, repo_def)

#     if globals.repo.endswith("/"):
#         print(bcolors.FAIL +
#               "Please ensure your path does not end with `/`" + bcolors.FAIL)
#         repoHandler()
#     elif not globals.repo.startswith("https://"):
#         print(bcolors.FAIL +
#               "Please ensure your path begins with a `https://`" + bcolors.FAIL)
#         repoHandler()
#     elif globals.repo == "":
#         print(bcolors.FAIL + "Please ensure your path is not blank" + bcolors.FAIL)
#         repoHandler()
#     else:
#         globals.repo = subprocess.run(
#             ["echo "+globals.repo], capture_output=True, shell=True, text=True).stdout.strip()
#         subprocess.run(["clear"], shell=True)
#         branchHandler()
