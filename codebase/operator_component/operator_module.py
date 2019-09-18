from . import operator_class as OperatorClass

def createoperator(webaddress, erasize, retrylimit):

	return OperatorClass.DefineOperator(webaddress, erasize, retrylimit)

