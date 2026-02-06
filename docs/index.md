# Osmosis Installer

The Osmosis Installer is a Python-based CLI tool that provides an easy and streamlined way to install and configure Osmosis blockchain nodes and clients. It is hosted at [get.osmosis.zone](https://get.osmosis.zone).

## Overview

```kroki-mermaid
flowchart TB
    User["User"] -->|curl get.osmosis.zone/run| Script["osmosis-installer.sh"]
    Script -->|downloads & runs| Installer["i.py - Python Installer"]
    
    Installer --> Choice{Installation Type}
    
    Choice -->|node| Node["Node Setup"]
    Choice -->|client| Client["Client Setup"]
    
    Node --> Binary["Download osmosisd binary"]
    Node --> Genesis["Download genesis.json"]
    Node --> Addrbook["Download addrbook"]
    Node --> Snapshot["Download & extract snapshot"]
    Node --> Cosmovisor["Setup Cosmovisor (optional)"]
    Node --> Service["Setup systemd service (optional)"]
    
    Client --> BinaryC["Download osmosisd binary"]
    Client --> Config["Configure RPC endpoint"]
```

## Quick Start

```bash
source <(curl -sL https://get.osmosis.zone/run)
```

!!! warning "Prerequisite"
    Requires `wget` and `python3` to be installed on the machine.

The installer will guide you interactively through the installation process. You can also use CLI flags to automate choices.

## Installation Types

| Type | Description | Use Case |
|------|-------------|----------|
| **node** | Full node installation with binary, genesis, addrbook, and snapshot | Running a validator or fullnode |
| **client** | Lightweight client setup with binary and RPC configuration | Querying the chain without running a node |
| **localosmosis** | Local development node | Development (not yet implemented) |

## Supported Networks

| Network | Chain ID | Current Version | RPC Endpoint |
|---------|----------|-----------------|--------------|
| **Mainnet** | `osmosis-1` | Auto-updated daily | `https://rpc.osmosis.zone` |
| **Testnet** | `osmo-test-5` | Auto-updated daily | `https://rpc.testnet.osmosis.zone` |

!!! info "Automatic Version Updates"
    The installer versions are automatically updated daily via a GitHub Actions workflow that checks the current chain versions from RPC endpoints and creates PRs when newer versions are detected.

## Supported Platforms

| OS | Architecture | Supported |
|----|-------------|-----------|
| **Linux** | amd64 | Yes |
| **Linux** | arm64 | Yes |
| **macOS** | amd64 (Intel) | Yes |
| **macOS** | arm64 (Apple Silicon) | Yes |

## CLI Flags

The installer supports the following flags for non-interactive usage:

| Flag | Short | Description | Values |
|------|-------|-------------|--------|
| `--install` | `-i` | Installation type | `node`, `client`, `localosmosis` |
| `--network` | `-n` | Network to join | `osmosis-1`, `osmo-test-5` |
| `--home` | | Osmosis home directory | Path (default: `~/.osmosisd`) |
| `--moniker` | `-m` | Node moniker | String (default: `osmosis`) |
| `--pruning` | `-p` | Pruning strategy | `default`, `nothing`, `everything` |
| `--cosmovisor` | `-c` | Install Cosmovisor | Flag |
| `--service` | `-s` | Setup systemd service (Linux only) | Flag |
| `--binary_path` | | Binary download path | Path (default: `/usr/local/bin`) |
| `--overwrite` | `-o` | Overwrite existing installation | Flag |
| `--verbose` | `-v` | Verbose output | Flag |

### Example: Non-Interactive Node Setup

```bash
python3 i.py \
  --install node \
  --network osmosis-1 \
  --home ~/.osmosisd \
  --moniker my-node \
  --pruning default \
  --cosmovisor \
  --service \
  --overwrite
```

### Example: Non-Interactive Client Setup

```bash
python3 i.py \
  --install client \
  --network osmosis-1 \
  --home ~/.osmosisd \
  --moniker my-client \
  --overwrite
```

## What the Installer Does

### Node Installation

1. **Installs dependencies** - Required system packages
2. **Downloads the osmosisd binary** - Correct version for the selected network and platform
3. **Initializes the node** - Creates config and data directories
4. **Downloads genesis.json** - From the official Osmosis storage
5. **Downloads addrbook** - For peer discovery
6. **Configures the node** - Peers, pruning, and other settings
7. **Downloads snapshot** - For fast sync (optional)
8. **Sets up Cosmovisor** - For automated upgrades (optional)
9. **Creates systemd service** - For background operation on Linux (optional)

### Client Installation

1. **Downloads the osmosisd binary** - Correct version for the selected network
2. **Initializes configuration** - Creates config directory
3. **Configures RPC endpoint** - Points to public RPC nodes

## Architecture

### Hosting

The installer is hosted on GitHub Pages with the custom domain `get.osmosis.zone`:

| URL | Content |
|-----|---------|
| `get.osmosis.zone` | Landing page (`index.html`) |
| `get.osmosis.zone/install` | Python installer script (`i.py`) |
| `get.osmosis.zone/run` | Shell wrapper (`osmosis-installer.sh`) |

### Binary Sources

Binaries are stored on DigitalOcean Spaces:

```
https://osmosis.fra1.digitaloceanspaces.com/binaries/v{VERSION}/osmosisd-{VERSION}-{OS}-{ARCH}
```

### CI/CD

```kroki-mermaid
flowchart LR
    subgraph Daily ["Daily Cron Job"]
        RPC["Query RPC<br/>abci_info"]
        Compare["Compare with<br/>i.py versions"]
        PR["Create PR<br/>if newer"]
    end

    subgraph OnPush ["On Push / PR"]
        Test["Test Installer<br/>Ubuntu + macOS"]
        Matrix["Matrix:<br/>osmosis-1, osmo-test-5"]
    end

    RPC --> Compare --> PR
    PR -->|merge| OnPush
    Test --> Matrix
```

| Workflow | Trigger | Description |
|----------|---------|-------------|
| **Update Installer** | Daily cron + manual | Checks RPC for new versions, creates PRs to update `MAINNET_VERSION` and `TESTNET_VERSION` |
| **Test Installer (Client)** | Push/PR to main/dev | Tests client installation on Ubuntu and macOS for both networks |

## Post-Installation Optimizations

### Adding Swap Space

For optimal performance, Osmosis nodes should have at least 64GB of RAM. If your system has less, set up swap space:

```bash
sudo swapoff -a
sudo fallocate -l <swap_size>G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo cp /etc/fstab /etc/fstab.bak
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Verify:

```bash
sudo swapon --show
```

### Increasing Open File Limits

```bash
# Edit limits.conf
sudo nano /etc/security/limits.conf

# Add:
* hard nofile 65536
* soft nofile 65536

# Edit common-session
sudo nano /etc/pam.d/common-session

# Add:
session required pam_limits.so
```

Restart the system after applying changes.

## Repository Structure

```
osmosis-installer/
├── .github/
│   └── workflows/
│       ├── test-client.yaml      # CI: test installer on Ubuntu/macOS
│       └── update-version.yaml   # Daily: auto-update chain versions
├── assets/
│   └── screenshot.png            # Terminal screenshot
├── CNAME                         # GitHub Pages domain (get.osmosis.zone)
├── favicon.png                   # Website favicon
├── i.py                          # Main Python installer script
├── index.html                    # Landing page for get.osmosis.zone
├── osmosis-installer.sh          # Shell wrapper (downloaded via /run)
├── docs/                         # This documentation
└── README.md
```

## Related Components

| Component | Relationship |
|-----------|-------------|
| [public-nodes-infra](https://github.com/osmosis-labs/public-nodes-infra) | Provides RPC/LCD endpoints used by the installer |
| [osmosis-nodes-infra](https://github.com/osmosis-labs/osmosis-nodes-infra) | Provides RPC/LCD endpoints used by the installer |
| [infrastructure](https://github.com/osmosis-labs/infrastructure) | Hosts snapshot service used for fast sync |
