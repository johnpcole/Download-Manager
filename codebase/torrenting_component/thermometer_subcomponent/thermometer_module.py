from ...fileprocessing_component.filesystem_subcomponent import filesystem_module as FileSystem
import os as OperatingSystem


# =========================================================================================
# Looks up the current temperature of the Raspberry Pi
# Returns the higher of the two values that are available,
# or 35.0 if the system is not unix
# =========================================================================================

def gettemperature():

	if FileSystem.concatenatepaths(" ", " ") == " / ":
		result = OperatingSystem.popen('vcgencmd measure_temp').readline()
		outcome = float(result[5:-3])
		result = OperatingSystem.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
		outcome2 = float(result) / 1000.0
		if outcome2 > outcome:
			outcome = outcome2
	else:
		outcome = 35.0
	return outcome

