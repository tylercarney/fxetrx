# status.py - Manages the status of the fxetrx service

import os
import sys
import json
import platform
import subprocess
import re
from datetime import datetime

CONFIG_FILE = "/etc/fxetrx/config.json" if platform.system().lower() == "linux" else "C:\\ProgramData\\fxetrx\\config.json"

def get_uptime():
    """Retrieve uptime of the fxetrx service based on the operating system."""
    system = platform.system().lower()
    try:
        if system == "windows":
            try:
                result = subprocess.run(["powershell", "-Command", "(Get-Process fxetrx).StartTime"], capture_output=True, text=True)
                if result.stdout.strip():
                    start_time = datetime.strptime(result.stdout.strip(), "%m/%d/%Y %I:%M:%S %p")
                    return (datetime.now() - start_time).total_seconds()
            except (FileNotFoundError, subprocess.SubprocessError):
                result = subprocess.run(["wmic", "process", "where", "name='fxetrx.exe'", "get", "CreationDate"], capture_output=True, text=True)
                match = re.search(r"(\d{14})", result.stdout)
                if match:
                    return match.group(1)  # Convert to elapsed seconds if needed
        elif system == "linux":
            result = subprocess.run(["ps", "-eo", "etimes,command"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "fxetrx" in line:
                    match = re.search(r"(\d+)", line)
                    if match:
                        return int(match.group(1))
        elif system == "darwin":
            result = subprocess.run(["ps", "-eo", "etime,command"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "fxetrx" in line:
                    match = re.search(r"(\d+):(\d+):(\d+)", line)
                    if match:
                        hours, minutes, seconds = map(int, match.groups())
                        return hours * 3600 + minutes * 60 + seconds
    except Exception:
        return None
    return None

def get_config_version():
    """Retrieve the version from the fxetrx configuration file."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("version")
    except Exception:
        return None
    return None

def check_service_status():
    """Check the status of the fxetrx service across different operating systems."""
    system = platform.system().lower()
    status_info = {
        "status": "unknown",
        "uptime": get_uptime(),
        "config_version": get_config_version(),
        "errors": []
    }
    
    try:
        if system == "windows":
            try:
                result = subprocess.run(["sc", "query", "fxetrx"], capture_output=True, text=True)
                output = result.stdout.lower()
            except FileNotFoundError:
                result = subprocess.run(["wmic", "service", "where", "name='fxetrx'", "get", "State"], capture_output=True, text=True)
                output = result.stdout.lower()
            if "running" in output:
                status_info["status"] = "running"
            elif "stopped" in output:
                status_info["status"] = "stopped"
            elif "paused" in output:
                status_info["status"] = "paused"
            else:
                status_info["status"] = "unknown"
        
        elif system == "linux":
            result = subprocess.run(["systemctl", "is-active", "fxetrx"], capture_output=True, text=True)
            output = result.stdout.strip().lower()
            if output == "active":
                status_info["status"] = "running"
            elif output == "inactive":
                status_info["status"] = "stopped"
            elif output == "failed":
                status_info["status"] = "failed"
            elif "not-found" in output:
                status_info["status"] = "not installed"
            else:
                status_info["status"] = "unknown"
        
        elif system == "darwin":  # macOS
            result = subprocess.run(["which", "launchctl"], capture_output=True, text=True)
            if result.returncode == 0:
                result = subprocess.run(["launchctl", "print", "system/fxetrx"], capture_output=True, text=True)
                if "running" in result.stdout:
                    status_info["status"] = "running"
                elif "stopped" in result.stdout:
                    status_info["status"] = "stopped"
                else:
                    result = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
                    if "fxetrx" in result.stdout:
                        status_info["status"] = "running"
                    else:
                        status_info["status"] = "unknown"
            else:
                status_info["status"] = "unknown"
                status_info["errors"].append("launchctl not found on this system")
        
        else:
            status_info["status"] = "not supported"
            status_info["errors"].append("Unsupported operating system")
    
    except FileNotFoundError:
        status_info["status"] = "not installed"
        status_info["errors"].append("Service not found")
    except Exception as e:
        status_info["errors"].append(str(e))
    
    return status_info

def main():
    """Main execution to check and print the service status in JSON format."""
    status_info = check_service_status()
    try:
        print(json.dumps(status_info, indent=4, ensure_ascii=False))
    except TypeError as e:
        print(json.dumps({"error": "Failed to serialize JSON", "details": str(e)}, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
