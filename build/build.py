#build.py - build fxetrx before installing as a service using the operating system's native service management tools
# start with checking if the service dependencies are installed
# if not, install them
# then build the service for the target operating system into the ./deployment directory
import os
import sys
import subprocess
import logging
import hashlib
import csv
import shlex

# Load build configuration
BUILD_CONFIG = "./build/build.conf"
MANIFEST_FILE = "./build/manifest.csv"
TEMP_DIR = "./build/temp/"


def load_build_config():
    """Load build configuration settings from build.conf with default values."""
    default_config = {
        "DEBUG": "0",
        "VERBOSE": "0",
        "build_command": [sys.executable, "build.py"]
    }
    config = default_config.copy()
    if os.path.exists(BUILD_CONFIG):
        with open(BUILD_CONFIG, "r") as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comments
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    logging.warning(f"Skipping malformed config line: {line}")
                    continue
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def calculate_sha256(file_path):
    """Calculate SHA256 hash of a given file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return "FILE_NOT_FOUND"
    except PermissionError:
        logging.error(f"Permission denied when accessing: {file_path}")
        return "PERMISSION_DENIED"
    except Exception as e:
        logging.error(f"Unexpected error accessing {file_path}: {e}")
        return "ERROR"


def cleanup_temporary_files():
    """Safely remove temporary build files without deleting unintended files."""
    if os.path.exists(TEMP_DIR):
        for root, dirs, files in os.walk(TEMP_DIR, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.startswith(TEMP_DIR):
                    try:
                        os.remove(file_path)
                        logging.info(f"Removed temporary file: {file_path}")
                    except Exception as e:
                        logging.error(f"Failed to remove {file_path}: {e}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if dir_path.startswith(TEMP_DIR):
                    try:
                        os.rmdir(dir_path)
                        logging.info(f"Removed temporary directory: {dir_path}")
                    except Exception as e:
                        logging.error(f"Failed to remove {dir_path}: {e}")
        try:
            os.rmdir(TEMP_DIR)
            logging.info(f"Removed temp directory: {TEMP_DIR}")
        except Exception as e:
            logging.error(f"Failed to remove temp directory: {e}")


def update_manifest():
    """Update manifest.csv with SHA256 hashes."""
    if not os.path.exists(MANIFEST_FILE):
        logging.error("Manifest file not found.")
        return
    
    temp_file = MANIFEST_FILE + ".tmp"
    with open(MANIFEST_FILE, "r", newline='') as infile, open(temp_file, "w", newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header if present
        header = next(reader, None)
        if header:
            writer.writerow(header)
        
        # Process each file entry
        for row in reader:
            if len(row) < 3 or any(not isinstance(item, str) for item in row):
                logging.warning(f"Skipping malformed line in manifest: {row}")
                continue
            try:
                file_path = row[0].strip()
                sha256_hash = calculate_sha256(file_path) if os.path.isfile(file_path) else "DIRECTORY"
                writer.writerow([file_path, sha256_hash, row[2].strip()])
            except IndexError:
                logging.warning(f"Skipping incomplete row in manifest: {row}")
                continue
    
    # Replace the old manifest with the updated one
    os.replace(temp_file, MANIFEST_FILE)


def build_service():
    """Build the service if needed based on configuration."""
    logging.info("Building the service...")
    config = load_build_config()
    build_command = config.get("build_command", [sys.executable, "build.py"])
    
    # Validate build command to ensure it's a list of strings
    if not isinstance(build_command, list) or any(not isinstance(cmd, str) for cmd in build_command):
        logging.error("Invalid build command configuration.")
        sys.exit(1)
    
    # Sanitize build command before execution
    sanitized_command = [shlex.quote(cmd) for cmd in build_command]
    logging.debug(f"Executing sanitized build command: {' '.join(sanitized_command)}")
    
    try:
        subprocess.run(sanitized_command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Build process failed: {e}")
        sys.exit(1)


def main():
    """Main function to execute the build process."""
    config = load_build_config()
    
    # Enable logging modes based on configuration
    if bool(int(config.get("DEBUG", "0"))):
        logging.info("Debug mode enabled")
    if bool(int(config.get("VERBOSE", "0"))):
        logging.info("Verbose output enabled")
    
    # Cleanup any leftover temp files before starting
    cleanup_temporary_files()
    
    # Update manifest and build the service
    update_manifest()
    build_service()
    
    logging.info("Build process completed successfully.")

if __name__ == "__main__":
    main()
