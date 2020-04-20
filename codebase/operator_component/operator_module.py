from . import operator_class as OperatorClass

def createoperator(webaddress, retrylimit):

	return OperatorClass.DefineOperator(webaddress, retrylimit)

