from . import triggering_class as TriggerClass


def createtrigger(webpageurl, erasize):
	return TriggerClass.DefineTrigger(webpageurl, erasize)

