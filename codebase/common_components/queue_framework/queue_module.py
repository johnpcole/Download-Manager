from . import queue_class as QueueClass



def createqueuewriter(location, hourstimelimit):
	newqueue = QueueClass.DefineQueue(location, "Queuer", hourstimelimit)
	return newqueue


def createqueuereader(location):
	newqueue = QueueClass.DefineQueue(location, "Reader", 0)
	return newqueue

