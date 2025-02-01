def install_service():
    """Install the service using the appropriate OS tools."""
    logging.info("Installing the service...")
    system = platform.system()
    if system == "Linux":
        subprocess.run(["sudo", "cp", "deployment/service_template", "/etc/systemd/system/fxetrx.service"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "fxetrx"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "fxetrx"], check=True)
    elif system == "Darwin":
        subprocess.run(["sudo", "cp", "deployment/service_template", "/Library/LaunchDaemons/com.fxetrx.plist"], check=True)
        subprocess.run(["sudo", "launchctl", "load", "/Library/LaunchDaemons/com.fxetrx.plist"], check=True)
        subprocess.run(["sudo", "launchctl", "start", "com.fxetrx"], check=True)
    elif system == "Windows":
        subprocess.run(["sc", "create", "fxetrx", "binPath=", os.path.join(os.getcwd(), "deployment", "fxetrx.exe")], check=True)
        subprocess.run(["sc", "start", "fxetrx"], check=True)
    else:
        logging.error("Unsupported operating system")
        sys.exit(1)
