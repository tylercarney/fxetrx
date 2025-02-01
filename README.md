# fxetrx - Fixes things and learns new tricks - very work in progres. Don't expect much, if anything, to work yet.

## Overview
fxetrx is a fully portable service that primarily compiles into optimized native code for the target operating system. However, it also supports running in an interpreted Python mode if configured to do so in the build system. This ensures flexibility for debugging and development while maintaining performance benefits for production environments.

fxetrx aims to have as much of its functionality compiled and optimized for the target platform as possible. However, the build system allows for an alternative mode where it runs as native Python, depending on the build configuration.

Regardless of build type, fxetrx includes:
- An embedded copy of the exact same Python version it was built with.
- A global collection of Python modules that plugins can use if they do not have their own virtual environments.
- A focus on avoiding excessive redundant disk usage while ensuring module version stability and avoiding conflicts.

## Quick Start
To install and start fxetrx quickly:
```sh
# Install and start fxetrx (Linux/macOS)
sudo python3 install.py && sudo systemctl start fxetrx
# Check status
python3 service/status.py
```
For **Windows**:
```powershell
# Install and start fxetrx
python install.py
sc start fxetrx
```

## Features
- **Cross-platform compatibility:** Runs on Windows, Linux, and macOS with dedicated service management implementations.
- **Modular architecture:** Uses OS-specific service handlers (`status_win.py`, `status_linux.py`, `status_mac.py`) for managing service status.
- **Automated service handling:** Install, start, stop, restart, and uninstall the service without manual intervention. Requires administrative or elevated privileges for installation and management of system services, ensuring secure execution.
- **Virtual Environment Support:** Each plugin operates within its own Python virtual environment.
- **Secure Communication:** The service runs on `127.0.0.1:7777` with HTTPS using a self-signed certificate generated during installation.
- **Comprehensive Logging:** Error handling and structured logging for debugging and monitoring.
- **Automated build and deployment:** Uses a build system that compiles and configures the service automatically.
- **Consistent API for Status Management:** Implements a base class (`StatusBase`) that ensures a unified interface across platforms.
- **Automated Testing and Validation:** Unit tests, integration tests, and system tests ensure service reliability.
- **Graceful Error Handling:** Detects missing dependencies and system mismatches early to prevent failures.
- **Secure Secret Management:** Uses the Python `keyring` module to handle all secrets, supporting OS-native keyrings and keystores, with platform-specific implementations.

## Compilation vs. Interpreted Execution
fxetrx supports **two execution modes**:
1. **Compiled Mode** (default) - Most of fxetrx is compiled into native binaries for optimized performance.
2. **Interpreted Mode** - Runs as native Python if specified in the build system, useful for debugging and development.

### How Build Configuration Determines Execution Mode
- The `build.conf` file specifies whether fxetrx should be compiled or run in native Python mode.
- By default, the compiled version includes:
  - The same Python version it was built with.
  - A global collection of Python modules for plugins.

## Keyring Integration Across OS
- **Windows:** Uses Windows Credential Manager for secure storage of secrets, integrating with the standard keyring APIs.
- **macOS:** Utilizes macOS Keychain for secure credential management, ensuring secrets persist securely within the native environment.
- **Linux:** Integrates with Secret Service API (e.g., GNOME Keyring, KWallet) to provide a secure and seamless credential storage experience.
- **Fallback Mechanisms:** If a platform lacks a supported keyring, fxetrx will securely prompt the user for credentials and allow manual configuration.

## Dependency Management
fxetrx ensures that all required dependencies are installed before execution. The installation process manages dependencies as follows:
- **Core Dependencies:** Installed within the fxetrx embedded Python environment to ensure consistent execution.
- **Plugin-Specific Dependencies:** Each plugin maintains its own virtual environment, avoiding conflicts between different versions of dependencies.
- **System-Level Dependencies:** If needed, system packages will be installed using OS-specific package managers (e.g., `apt`, `dnf`, `brew`, `winget`). However, the preference is to keep everything within the contained environment to avoid unnecessary system modifications.

## Privilege Management and Installation
- **Windows:** Uses `runas` or requires administrator permissions to install as a system service.
- **Linux/macOS:** Uses `sudo` and `systemd` (if available) for managing service installation.

## Status Management
Each OS has a dedicated `status_*.py` file that implements `StatusBase`. The correct implementation is dynamically loaded based on the detected OS in `status.py`. These implementations address OS-specific edge cases and failure scenarios:

- **Windows (`status_win.py`)**: Uses `sc query`, PowerShell, or WMIC to check service status. Implements fallback mechanisms for older Windows versions where some utilities may be unavailable.
- **Linux (`status_linux.py`)**: Uses `systemctl is-active` for modern Linux distributions and gracefully handles cases where `systemd` is not present by falling back to alternative process checks.
- **macOS (`status_mac.py`)**: Uses `launchctl print` for detailed service information and falls back to `launchctl list` when necessary to support multiple macOS versions.

### `StatusBase` Class (Defined in `status.py`)
- `get_uptime()`: Returns the service uptime.
- `check_service_status()`: Retrieves service status in JSON format.
- `custom_serializer()`: Handles serialization of non-serializable objects like datetime and sets.

## Troubleshooting
### Issue: Permission denied when starting fxetrx
**Solution:** Ensure you have admin privileges. Use `sudo` on Linux/macOS or `runas` on Windows.

### Issue: Service fails to start
**Solution:** Check `logs/` directory for errors. Run `service/status.py` for diagnostics.

### Issue: Missing dependencies
**Solution:** Run `install.py` again to ensure all dependencies are correctly installed.

### Issue: Keyring authentication fails
**Solution:** Ensure the keyring backend is properly configured. Use `keyring --list-backends` to check available keyring options.

## Installation Process
- Ensures required dependencies are installed within the fxetrx-contained Python environment.
- Builds and optimizes the service.
- Verifies installation and starts the service.
- Supports full uninstallation and cleanup.

## Summary
fxetrx provides a unified, cross-platform service management framework with modular design and automation capabilities. With planned enhancements, it aims to be an extensible and robust solution for service deployment.
