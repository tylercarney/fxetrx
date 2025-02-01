import subprocess
import re
from datetime import datetime
from service.status import StatusBase

class WindowsStatus(StatusBase):
    """Windows-specific implementation of the fxetrx service status interface."""
    
    def get_uptime(self):
        """Retrieve the uptime of the fxetrx service on Windows."""
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
        return None
    
    def check_service_status(self):
        """Check the status of the fxetrx service on Windows."""
        status_info = {
            "status": "unknown",
            "uptime": self.get_uptime(),
            "errors": []
        }
        try:
            result = subprocess.run(["sc", "query", "fxetrx"], capture_output=True, text=True)
            output = result.stdout.lower()
            if "running" in output:
                status_info["status"] = "running"
            elif "stopped" in output:
                status_info["status"] = "stopped"
            elif "paused" in output:
                status_info["status"] = "paused"
            else:
                status_info["status"] = "unknown"
        except FileNotFoundError:
            status_info["status"] = "not installed"
            status_info["errors"].append("Service not found")
        except Exception as e:
            status_info["errors"].append(str(e))
        
        return status_info
