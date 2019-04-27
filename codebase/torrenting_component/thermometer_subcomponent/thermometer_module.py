from ...fileprocessing_component.filesystem_subcomponent import filesystem_module as FileSystem
import os as OperatingSystem

def gettemperature():
    if FileSystem.concatenatepaths(" ", " ") == " / ":
        result = OperatingSystem.popen('vcgencmd measure_temp').readline()
        outcome = float(result[5:-3])
        result = OperatingSystem.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
        outcome2 = float(result) / 1000.0
        if outcome2 > outcome:
            outcome = outcome2
    else:
        outcome = 45.0
    return outcome

