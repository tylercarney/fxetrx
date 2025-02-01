#dependency_manager.py - manages dependencies for fxetrx and its plugins


def check_dependencies():
    """Check if required dependencies are installed."""
    logging.info("Checking service dependencies...")
    fxetrx_python = setup_fxetrx_venv()
    subprocess.run([fxetrx_python, "-m", "pip", "install", "-r", "core_requirements.txt"], check=True)
    
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        logging.warning("Plugins directory not found. Skipping venv setup.")
        return
    
    for plugin in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin)
        if os.path.isdir(plugin_path):
            venv_path = os.path.join(plugin_path, "venv")
            if not os.path.exists(venv_path):
                logging.info(f"Creating virtual environment for {plugin}...")
                venv.create(venv_path, with_pip=True)
            
            logging.info(f"Installing dependencies for {plugin}...")
            subprocess.run([os.path.join(venv_path, "bin", "pip"), "install", "-r", os.path.join(plugin_path, "requirements.txt")], check=True)

