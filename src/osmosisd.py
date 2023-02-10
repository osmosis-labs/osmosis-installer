import subprocess
import globals
from style import colorprint, bcolors
from complete import complete, completeOsmosisd, completeCosmovisor


def osmosisdService():
    colorprint("Creating Osmosisd Service...")
    subprocess.run(["""echo '[Unit]
Description=Osmosis Daemon
After=network-online.target
[Service]
User =""" + globals.USER+"""
ExecStart="""+globals.HOME+"""/go/bin/osmosisd start --home """+globals.osmo_home+"""
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
Environment=\"DAEMON_HOME="""+globals.osmo_home+"""\"
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
[Install]
WantedBy=multi-user.target
' >osmosisd.service
    """], shell=True, env=globals.selected_my_env)
    subprocess.run(
        ["sudo mv osmosisd.service /lib/systemd/system/osmosisd.service"], shell=True, env=globals.selected_my_env)
    subprocess.run(["sudo systemctl daemon-reload"],
                   shell=True, env=globals.selected_my_env)
    subprocess.run(["systemctl restart systemd-journald"],
                   shell=True, env=globals.selected_my_env)
