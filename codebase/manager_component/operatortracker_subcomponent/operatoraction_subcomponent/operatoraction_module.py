from . import operatoraction_class as OperatorActionClass


def createaoperatoraction(action, context):
	return OperatorActionClass.DefineOperatorActionItem(action, context)

