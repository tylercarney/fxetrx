# fxetrx Installed Application Structure

This document outlines the **file and application structure** after fxetrx has been installed on a system. Since fxetrx is designed to be cross-platform, the installation locations will vary depending on the operating system.

## Installation Locations per OS
### **Linux (systemd-based distributions)**
- Installed in: `/opt/fxetrx/` (default) or `/usr/local/fxetrx/`
- Service registered with `systemd`: `/etc/systemd/system/fxetrx.service`
- Logs stored in: `/var/log/fxetrx/`
- Configuration stored in: `/etc/fxetrx/`

### **macOS**
- Installed in: `/Library/Application Support/fxetrx/`
- Service managed by `launchctl`
- Logs stored in: `/Library/Logs/fxetrx/`
- Configuration stored in: `/Library/Preferences/fxetrx/`

### **Windows**
- Installed in: `C:\Program Files\fxetrx\` or `C:\fxetrx\`
- Service registered with `sc.exe`
- Logs stored in: `C:\ProgramData\fxetrx\logs\`
- Configuration stored in: `C:\ProgramData\fxetrx\config\`

## Installed Directory Layout
```
fxetrx/
│── bin/                  # Compiled/optimized binaries
│   ├── fxetrx            # Main executable (fxetrx.exe on Windows)
│   ├── helper_tools/     # Additional utilities
│
│── lib/                  # Core Python modules
│   ├── keyring/
│   ├── requests/
│   ├── core_modules/     # Always available modules
│
│── python/               # Embedded Python runtime
│   ├── python3.x/        # Version that matches build
│   ├── site-packages/
│
│── plugins/              # Plugin system
│   ├── venvs/            # Virtual environments for plugins
│   ├── plugin1/
│   ├── plugin2/
│
│── config/               # Configuration files
│   ├── fxetrx.conf       # Main configuration file
│   ├── certificates/     # Self-signed HTTPS certificates
│
│── logs/                 # Service logs
│
│── service/              # Service management scripts
│   ├── start.sh          # Start script (start.bat for Windows)
│   ├── stop.sh           # Stop script (stop.bat for Windows)
│   ├── restart.sh        # Restart script
│   ├── status.sh         # Status check script
│
│── data/                 # Service data storage
```

## Key Directories and Files
### **bin/**
- Contains the compiled service binaries and helper tools.
- Ensures a lightweight and optimized execution environment.

### **lib/**
- Stores core Python modules available to the service and plugins.
- Provides necessary functionality without requiring global Python installs.

### **python/**
- Contains an **embedded** Python runtime to ensure consistency.
- Guarantees the same Python version as used during the build process.

### **plugins/**
- Each plugin runs in its own virtual environment to prevent conflicts.
- Plugin dependencies are isolated within `venvs/`.

### **config/**
- Stores service configuration settings.
- Includes self-signed certificates for encrypted communication.

### **logs/**
- Maintains structured logs for debugging and monitoring.

### **service/**
- Manages the lifecycle of fxetrx via OS-specific service control scripts.
- Scripts handle starting, stopping, restarting, and checking service status.

### **data/**
- Storage location for service-generated and managed data.

## Speculative Enhancements
- **Automated Installers**: Provide `.deb`, `.rpm`, `.msi`, and `.pkg` packages for seamless installation.
- **Configuration Wizard**: Offer an interactive first-run experience to guide users through setup.
- **Containerization**: Add optional Docker and Kubernetes deployment configurations.
- **API Endpoint for Management**: Provide a local HTTP API for interacting with the service.

---

This document provides a reference for developers and administrators maintaining an installed fxetrx instance. The structure aims to keep installations consistent across platforms while allowing OS-specific optimizations.
