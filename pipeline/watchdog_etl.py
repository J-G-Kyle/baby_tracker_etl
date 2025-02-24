import subprocess
import sys
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import time
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


class Handler(PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(
            self, patterns=["*.csv"], ignore_directories=True, case_sensitive=False
        )

    def on_created(self, event):
        # Event is created, you can process it now
        new_file = event.src_path  # Get the full path of the new file
        logging.info(f"Watchdog received a created event - {event.src_path}")

        # Trigger the new csv Python script with the new file name
        module_directory = Path(__file__).parent
        relative_path_to_new_csv_import = "new_csvs.py"
        source_path = module_directory / relative_path_to_new_csv_import
        subprocess.run(
            ["python3", str(source_path), new_file],
            check=True,
            capture_output=False,
        )
        # Is the watchdog process interrupted and this needs to run as a background job???
        logger.info(
            "Refreshing Evidence sources and rebuilding queries with updated data"
        )

    # def on_modified(self, event):
    # 	print("Watchdog received modified event - % s." % event.src_path)
    # 	# Event is modified, you can process it now


if __name__ == "__main__":
    src_path = "/evidence/data/"
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=False)
    observer.start()
    logger.info(f"Watchdog process started, observing {src_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
