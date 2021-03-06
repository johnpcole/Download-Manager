from . import monitoring_class as MonitoringClass
from ...common_components.datetime_datatypes import datetime_module as DateTime



def createmonitor():
	return MonitoringClass.DefineMonitor()



def getloadlist():
	timedate = DateTime.getnow()
	timedate.adjustdays(-12)
	outcome = []
	for index in range(0, 12):
		timedate.adjustdays(1)
		outcome.append(timedate.getdateiso())

	return outcome
