# install.py - Orchestrates the installation of fxetrx as a service

# # This script primarily coordinates the installation process by delegating tasks
# # to other modules, ensuring a modular and maintainable approach.
# #
# # fxetrx is fully portable and compiles to native optimized code for the target operating system.
# # It utilizes the operating system's native tools through an internal abstraction layer,
# # providing a consistent target API for fxetrx plugins, keeping the codebase clean and maintainable.
# #
# # The service can be installed, started, stopped, restarted, and uninstalled from any location,
# # consuming minimal resources.
# #
# # The installation process includes installing core service dependencies.
# # Each fxetrx plug-in has its own Python virtual environment, and dependencies are managed separately.
# #
# # Once running, fxetrx listens on a port for incoming requests, defaulting to 127.0.0.1:7777,
# # and processes them as needed. It employs HTTPS with a self-signed certificate,
# # generated during installation.
# #
# # Installation steps include:
# # - Checking if dependencies are installed
# # - Building the service (if necessary) into the ./deployment directory
# # - Verifying the build by executing relevant test suites in ./tests
# # - Installing the service using the operating system's service management tools
# # - Checking service status and verifying expected failures/successes at various stages
# # - Automating the process while allowing user selection of the destination directory,
# #   defaulting to the OS's standard third-party service directory.

import os
import sys
import subprocess
import logging
import time
import json
from src.dependency_manager import check_dependencies
from build.venv_setup import setup_venvs
from service.install_service import install_service
from build.build import load_build_config, verify_build

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_status(expected_running=False):
    """Check if the service is installed and running, verifying uptime if expected to be running."""
    result = subprocess.run([sys.executable, "service/status.py"], capture_output=True, text=True, check=False)
    logging.info(f"Service status output:\n{result.stdout}")
    
    if result.returncode != 0:
        logging.warning(f"Service status check failed with error:\n{result.stderr}")
        return False
    
    try:
        status_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        logging.error("Failed to parse service status JSON output.")
        return False
    
    if expected_running:
        uptime = status_data.get("uptime")
        if uptime is None or not isinstance(uptime, int) or uptime > 5:  # Assuming service should have just started
            logging.warning("Service uptime is longer than expected, possible issue.")
            return False
    return True

def start_service():
    """Start the service and verify it starts correctly."""
    logging.info("Starting the service...")
    result = subprocess.run([sys.executable, "service/start.py"], capture_output=True, text=True, check=False)
    logging.info(f"Start service output:\n{result.stdout}")
    if result.returncode != 0:
        logging.error(f"Service failed to start:\n{result.stderr}")
        sys.exit(1)
    time.sleep(2)  # Allow time for the service to initialize
    if not check_status(expected_running=True):
        logging.error("Service did not start correctly.")
        sys.exit(1)

def stop_service():
    """Stop the service and verify it stops correctly."""
    logging.info("Stopping the service...")
    result = subprocess.run([sys.executable, "service/stop.py"], capture_output=True, text=True, check=False)
    logging.info(f"Stop service output:\n{result.stdout}")
    if result.returncode != 0:
        logging.warning(f"Service failed to stop:\n{result.stderr}")
    if check_status():
        logging.error("Service is still running after stop command. Additional details: "
                      f"Output:\n{result.stdout}\nError:\n{result.stderr}")
        sys.exit(1)

def uninstall_service():
    """Uninstall the service and verify all traces are removed."""
    logging.info("Uninstalling the service...")
    result = subprocess.run([sys.executable, "uninstall.py"], capture_output=True, text=True, check=False)
    logging.info(f"Uninstall service output:\n{result.stdout}")
    if result.returncode != 0:
        logging.warning(f"Service uninstallation may not be complete:\n{result.stderr}")
    if check_status():
        logging.error("Service is still detected after uninstallation.")
        sys.exit(1)

def main():
    try:
        config = load_build_config()
        check_dependencies()
        setup_venvs()
        
        logging.info("Building the service...")
        verify_build()
        install_service()
        
        if check_status():
            logging.error("Service should not be running immediately after install.")
            sys.exit(1)
        
        start_service()
        stop_service()
        uninstall_service()
        
        logging.info("Reinstalling to leave the service in place.")
        install_service()
        start_service()
        
        logging.info("Installation process completed successfully.")
    except FileNotFoundError as e:
        logging.error(f"File not found error: {e}")
        sys.exit(1)
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        sys.exit(1)
    except subprocess.SubprocessError as e:
        logging.error(f"Subprocess execution error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
