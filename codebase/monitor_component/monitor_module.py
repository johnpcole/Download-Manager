from . import monitor_class as MonitorClass


def createtrigger(webpageurl, erasize):
	return MonitorClass.DefineTrigger(webpageurl, erasize)

