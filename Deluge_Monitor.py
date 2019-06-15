from codebase.common_components.logging_framework import logging_module as Logging
from codebase.triggering_component import triggering_module as Trigger







Logging.printrawline("Starting Download-Manager Application")

trigger = Trigger.createtrigger("http://127.0.0.1:5000/TriggerDelugeMonitor", 2)

while 1 != 0:

	trigger.refresh()

Logging.printrawline("Ending Download-Manager Application")

