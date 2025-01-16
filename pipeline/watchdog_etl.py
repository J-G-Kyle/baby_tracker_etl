import subprocess
import watchdog.events
import watchdog.observers
import time
import logging
logger = logging.getLogger(__name__)

class Handler(watchdog.events.PatternMatchingEventHandler):
	def __init__(self):
		# Set the patterns for PatternMatchingEventHandler
		watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.csv'],
															ignore_directories=True, case_sensitive=False)

	def on_created(self, event):
		# Event is created, you can process it now
		new_file = event.src_path  # Get the full path of the new file
		logging.info(f"Watchdog received a created event - {event.src_path}")

		# Trigger the new csv Python script with the new file name
		subprocess.run(["python", "new_csvs.py", new_file])

	# def on_modified(self, event):
	# 	print("Watchdog received modified event - % s." % event.src_path)
	# 	# Event is modified, you can process it now


if __name__ == "__main__":
	src_path = r"../assets/data/"
	event_handler = Handler()
	observer = watchdog.observers.Observer()
	observer.schedule(event_handler, path=src_path, recursive=False)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
