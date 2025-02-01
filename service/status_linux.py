import subprocess
import re
from datetime import datetime
from service.status import StatusBase

class LinuxStatus(StatusBase):
    """Linux-specific implementation of the fxetrx service status interface."""
    
    def get_uptime(self):
        """Retrieve the uptime of the fxetrx service on Linux."""
        try:
            result = subprocess.run(["ps", "-eo", "etimes,command"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "fxetrx" in line:
                    match = re.search(r"(\d+)", line)
                    if match:
                        return int(match.group(1))
        except Exception:
            return None
        return None
    
    def check_service_status(self):
        """Check the status of the fxetrx service on Linux."""
        status_info = {
            "status": "unknown",
            "uptime": self.get_uptime(),
            "errors": []
        }
        try:
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
        except FileNotFoundError:
            status_info["status"] = "not installed"
            status_info["errors"].append("Service not found")
        except Exception as e:
            status_info["errors"].append(str(e))
        
        return status_info
