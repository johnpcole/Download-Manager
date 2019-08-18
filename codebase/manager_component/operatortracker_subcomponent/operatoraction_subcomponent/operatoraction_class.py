from .....common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineOperatorActionItem:

	def __init__(self, actiontype, context):


		self.actiontype = Enumeration.createenum(["Add", "Delete", "Start", "Stop", "Refresh"], actiontype)

		self.context = context

# =========================================================================================

	def getinstruction(self):

		return {'action': self.actiontype.displaycurrent(), 'context': self.context}

