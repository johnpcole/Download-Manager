from ..filesystem_framework import filesystem_module as FileSystem
import os as OperatingSystem


# =========================================================================================
# Looks up the current temperature of the Raspberry Pi
# Returns the higher of the two values that are available,
# or 35.0 if the system is not unix
# =========================================================================================

def getoveralltemperature():

	templist = gettemperatures()

	outcome = -999.9

	for tempitem in templist:

		outcome = max(outcome, tempitem)

	return outcome


def gettemperatures():

	outcome = []

	if FileSystem.concatenatepaths(" ", " ") == " / ":

		result = OperatingSystem.popen('vcgencmd measure_temp').readline()
		outcome.append(float(result[5:-3]))

		result = OperatingSystem.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
		outcome.append(float(result) / 1000.0)

	else:
		outcome.append(-999.9)
		outcome.append(-999.9)

	return outcome
