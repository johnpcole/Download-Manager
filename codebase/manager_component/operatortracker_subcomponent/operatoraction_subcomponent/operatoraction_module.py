from . import operatoraction_class as OperatorActionClass


def createaoperatoraction(action, context):
	return OperatorActionClass.DefineOperatorActionItem(action, context)


def createfromexisting(existingobject):
	data = existingobject.getinstruction()
	return OperatorActionClass.DefineOperatorActionItem(data['action'], data['context'])




