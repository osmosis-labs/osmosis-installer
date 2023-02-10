import subprocess
from style import bcolors, colorprint
from snapshots import snapshotInstall, infraSnapshotInstall


def mainNetLocation(args):
    global location
    location_map = {"1": "Netherlands", "2": "Singapore", "3": "SanFrancisco"}
    colorprint("""Please choose the location nearest to your node:
1) Netherlands
2) Singapore
3) SanFrancisco (WARNING: Location usually slow)
    """)
    nodeLocationAns = get_key_case_insensitive(
        location_map, args.snapshotLocation)
    if nodeLocationAns == None:
        nodeLocationAns = input(
            bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    subprocess.run(["clear"], shell=True)
    if nodeLocationAns in location_map:
        location = location_map[nodeLocationAns]
        snapshotInstall(args)
    else:
        mainNetLocation(args)


def get_key_case_insensitive(dict, candidate_value):
    if candidate_value is None:
        return None
    candidate = candidate_value.lower()
    key = [k for k, v in dict.items() if v.lower() == candidate]
    if len(key) == 1:
        return key[0]
    return None
