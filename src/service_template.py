# service_template.py - A template for creating a cross-platform service in Python
# created for fxetrx
import sys
import time
import logging
import threading
import platform
import os

# Configure logging to write to a file, overwriting existing logs on each run
logging.basicConfig(
    filename="service.log",
    filemode='w',  # Overwrite log file on each run
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def service_task(service):
    """
    Main service loop that runs in a separate thread.
    Continuously logs that the service is running until stopped.
    """
    while service.running:
        logging.info("Service is running...")
        time.sleep(10)  # Simulate background processing with a delay

class CrossPlatformService:
    """
    A simple cross-platform service implementation that can be started and stopped.
    Uses a background thread to run the service task.
    """
    def __init__(self):
        self.running = False  # Flag to indicate if the service is active
        self.thread = None  # Thread reference for running the service

    def start(self):
        """
        Start the service if it's not already running.
        Spawns a new thread to run the service task.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=service_task, args=(self,), daemon=True)
            self.thread.start()
            logging.info("Service started")

    def stop(self):
        """
        Stop the service and ensure the background thread terminates.
        """
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()  # Ensure the thread is properly stopped
            logging.info("Service stopped")

if __name__ == "__main__":
    service = CrossPlatformService()
    if len(sys.argv) > 1:
        # Command-line interface to start or stop the service
        if sys.argv[1] == "start":
            service.start()
        elif sys.argv[1] == "stop":
            service.stop()
        else:
            print("Usage: python service.py [start|stop]")
    else:
        # If no arguments provided, start the service manually
        service.start()
        while service.running:
            try:
                time.sleep(1)  # Keep the main thread alive while the service runs
            except KeyboardInterrupt:
                logging.info("Service is exiting due to keyboard interrupt")
                service.stop()
                sys.exit(0)
