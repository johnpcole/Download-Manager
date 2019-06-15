from . import delayer_class as DelayerClass


def createdelayer(erasize):
	return DelayerClass.DefineDelayer(erasize)

