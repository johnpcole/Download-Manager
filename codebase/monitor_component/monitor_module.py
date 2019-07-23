from . import monitor_class as MonitorClass


def createtrigger(webpageurl, erasize, retrylimit):
	return MonitorClass.DefineTrigger(webpageurl, erasize, retrylimit)

