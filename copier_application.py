from codebase.common_components.logging_framework import logging_module as Logging
from codebase.copier_component import copier_module as Copier




Logging.printrawline("Starting Download-Copier Application")

# Use 1 for second updates
# Use 2 for ten-second updates
# Use 3 for minute updates
# Use 4 for ten-minute updates

copier = Copier.createcopier("http://127.0.0.1:5000/TriggerDownloadCopier", 3, 3)

while 1 != 0:

	copier.refresh()


Logging.printrawline("Ending Download-Copier Application")

