from codebase.common_components.logging_framework import logging_module as Logging
from codebase.operator_component import operator_module as Operator







Logging.printrawline("Starting Download-Operator Application")

operator = Operator.createoperator()

while 1 != 0:

	operator.refresh()

Logging.printrawline("Ending Download-Operator Application")

