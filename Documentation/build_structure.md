# fxetrx Build Environment Structure

This document describes the structure of the **build environment** for fxetrx, including the files and directories used during the build process before deployment.

## Build Directory Layout
```
fxetrx/
│── build/                  # Main build directory containing all build-related scripts and configurations
│   ├── build.conf          # Build configuration file controlling the build process
│   ├── build.py            # Primary script that orchestrates the build process
│   ├── manifest.csv        # Lists built files with SHA-256 hashes for integrity verification
│   ├── venv_setup.py       # Script for setting up virtual environments
│   ├── temp_dir/           # Temporary directory for intermediate build artifacts
│
│── deployment/             # Deployment artifacts before installation
│
│── install.py              # Service installation script
│── uninstall.py            # Service uninstallation script
│
│── service/                # Service management files
│   ├── install_service.py  # Handles service installation process
│   ├── restart.py          # Restarts the service
│   ├── start.py            # Starts the service
│   ├── stop.py             # Stops the service
│   ├── status.py           # Base service status logic
│   ├── status_linux.py     # Linux-specific status implementation
│   ├── status_mac.py       # macOS-specific status implementation
│   ├── status_win.py       # Windows-specific status implementation
│
│── src/                    # Core functionality
│   ├── dependency_manager.py  # Manages dependencies for the service
│   ├── plugin_venv_setup.py   # Handles plugin virtual environment setup
│   ├── service_template.py    # Base template for service functionality
│
│── tests/                  # Unit and integration test scripts
```

### **build.conf** (Build Configuration File)
- Controls how the build process executes.
- Specifies whether to compile fxetrx or run it as interpreted Python.
- Configurable settings include:
  - **Debug Mode:** Enables verbose output for debugging.
  - **Optimization Flags:** Controls performance tuning and stripping unnecessary components.
  - **Packaging Options:** Determines whether installation packages should be created.
  - **Platform-Specific Configurations:** Tailors the build for Windows, Linux, or macOS.

### **build.py** (Build Orchestration Script)
- Reads `build.conf` and determines the build process flow.
- Performs the following key steps:
  1. **Checks dependencies** and ensures required tools are installed.
  2. **Runs venv_setup.py** to prepare virtual environments.
  3. **Compiles or packages the application** according to `build.conf` settings.
  4. **Generates manifest.csv** for tracking built files.
  5. **Prepares artifacts for deployment.**

### **manifest.csv** (Build Manifest File)
- Lists every generated file along with its SHA-256 hash.
- Used to verify build integrity before deployment.
- Helps in detecting any corruption or tampering of built artifacts.

### **venv_setup.py** (Virtual Environment Setup)
- Handles creation and management of Python virtual environments.
- Installs necessary dependencies for:
  - **Core fxetrx functionality.**
  - **Plugin support modules.**
  - **Cross-platform execution requirements.**
- Ensures all installed packages match version requirements from `build.conf`.

### **temp_dir/** (Temporary Build Directory)
- Stores intermediate build artifacts such as:
  - **Temporary compilation files** (if applicable).
  - **Extracted resources** for packaging.
  - **Pre-processed dependencies** before deployment.
- **Auto-cleans after build completion** to prevent unnecessary disk usage.

## Deployment Artifacts Directory
The **deployment/** directory contains the compiled and prepared package before installation. Artifacts generated here include:
- The **final compiled binary** or Python runtime package.
- Configuration files necessary for running fxetrx.
- Pre-packaged installation files if specified in `build.conf`.
- Any additional support tools required by the service.

When `install.py` is executed, these artifacts are moved to their appropriate locations in the final installation directory.

---

This document serves as a reference for contributors working on the fxetrx build process, ensuring clarity on the role of each component in the build workflow.
