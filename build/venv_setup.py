#venv_setup.py - setup the virtual environment for the build process

def setup_fxetrx_venv():
    """Ensure fxetrx has a dedicated Python installation and environment."""
    venv_path = os.path.join(os.getcwd(), "fxetrx_venv")
    if not os.path.exists(venv_path):
        logging.info("Creating dedicated fxetrx virtual environment...")
        venv.create(venv_path, with_pip=True)
    return os.path.join(venv_path, "bin", "python") if platform.system() != "Windows" else os.path.join(venv_path, "Scripts", "python.exe")
