import subprocess
import re
from datetime import datetime
from service.status import StatusBase

class MacOSStatus(StatusBase):
    """MacOS-specific implementation of the fxetrx service status interface."""
    
    def get_uptime(self):
        """Retrieve the uptime of the fxetrx service on macOS."""
        try:
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
    
    def check_service_status(self):
        """Check the status of the fxetrx service on macOS."""
        status_info = {
            "status": "unknown",
            "uptime": self.get_uptime(),
            "errors": []
        }
        try:
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
        except FileNotFoundError:
            status_info["status"] = "not installed"
            status_info["errors"].append("Service not found")
        except Exception as e:
            status_info["errors"].append(str(e))
        
        return status_info
