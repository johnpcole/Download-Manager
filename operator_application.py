from codebase.common_components.logging_framework import logging_module as Logging
from codebase.operator_component import operator_module as Operator
from codebase import file_locations as Locations





Logging.printrawline("Starting Download-Operator Application")

operator = Operator.createoperator(Locations.operatoractionqueue(),
									Locations.sessiondataqueue(),
									Locations.operatorapplicationconfiguration(),
									Locations.historydataqueue())

while 1 != 0:

	operator.refresh()

Logging.printrawline("Ending Download-Operator Application")

