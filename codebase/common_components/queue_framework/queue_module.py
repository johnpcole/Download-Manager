from . import queue_class as QueueClass



def createqueue(location, role):
	newqueue = QueueClass.DefineQueue(location, role)
	return newqueue


