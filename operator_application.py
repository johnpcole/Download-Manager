from codebase.common_components.logging_framework import logging_module as Logging
from codebase.operator_component import operator_module as Operator







Logging.printrawline("Starting Download-Operator Application")

# Use 1 for second updates
# Use 2 for ten-second updates
# Use 3 for minute updates
# Use 4 for ten-minute updates

operator = Operator.createoperator("http://127.0.0.1:5000/TriggerDownloadOperator", 4, 3)

while 1 != 0:

	operator.refresh()

Logging.printrawline("Ending Download-Operator Application")

