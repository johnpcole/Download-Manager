from common_components.logging_framework import logging_module as Logging
from common_components.delayer_framework import delayer_module as Delayer







Logging.printrawline("Starting Download-Copier Application")

# Use 1 for second updates
# Use 2 for ten-second updates
# Use 3 for minute updates
# Use 4 for ten-minute updates

delayer = Delayer.createdelayer(3)

while 1 != 0:

	if delayer.checkdelay() == True:
		# do some copying!
		delayer.waitlong()
	else:
		delayer.waitshort()

Logging.printrawline("Ending Download-Copier Application")

