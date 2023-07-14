# Osmosis Installer

<p align="center">
  <img src="assets/screenshot.png" alt="Screenshot">
</p>

The Osmosis Installer is a simple tool that provides an easy and streamlined way to install and configure Osmosis.

## ✨ Features

The Osmosis Installer offers the following key features:

🔧 **Dependency Installation**: Automatically installs the necessary dependencies for running Osmosis.

🌐 **Network Joining**: Allows you to choose between joining the testnet or mainnet.

⬇️ **Binary Download**: Downloads the Osmosis binary for the selected network.

⚙️ **Configuration Customization**: Provides options for customizing your Osmosis configuration.

🔌 **Background Service Setup**: Sets up either cosmovisor or osmosisd as background services for continuous operation.

##  Installation

To install Osmosisd, follow these steps:

1. Open your terminal.

2. Run the following command:

```bash
source <(curl -sL https://get.osmosis.zone/run)
```

This command will download and execute the Osmosis Installer script.

Follow the on-screen instructions to complete the installation. The installer will guide you through the installation process, allowing you to make choices such as selecting the installation type (node or client) and customizing various settings.

> 💡 Optional Flags:
> You can use some flag to specify the choices. For example, if you want to install the node, you can use the `--install node` flag. If you want to install the client, you can use the `--install client` flag.