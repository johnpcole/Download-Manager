from . import operator_class as OperatorClass

def createoperator(operatorqueuelocation, sessiondataqueuelocation, operatorconfiglocation, historydatalocation):

	return OperatorClass.DefineOperator(operatorqueuelocation, sessiondataqueuelocation, operatorconfiglocation,
																									historydatalocation)

