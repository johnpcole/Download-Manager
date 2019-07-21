from codebase.common_components.logging_framework import logging_module as Logging
from codebase.monitor_component import monitor_module as Trigger







Logging.printrawline("Starting Download-Monitor Application")

# Use 1 for second updates
# Use 2 for ten-second updates
# Use 3 for minute updates
# Use 4 for ten-minute updates

trigger = Trigger.createtrigger("http://127.0.0.1:5000/TriggerDownloadMonitor", 4, 3)

while 1 != 0:

	trigger.refresh()

Logging.printrawline("Ending Download-Monitor Application")

