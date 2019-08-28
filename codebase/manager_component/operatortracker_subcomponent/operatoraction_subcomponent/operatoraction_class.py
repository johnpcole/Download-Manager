from ....common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineOperatorActionItem:

	def __init__(self, actiontype, context):


		self.actiontype = Enumeration.createenum(["Add", "Delete", "Start", "Stop", "Refresh"], actiontype)

		self.context = context

# =========================================================================================

	def getinstruction(self, index):

		return {'index': index, 'action': self.actiontype.displaycurrent(), 'context': self.context}

# =========================================================================================

	def isrefresh(self):

		return self.actiontype.get("Refresh")


	def isduplicate(self, action, context):

		if (self.actiontype.get(action) == True) and (self.context == context):
			outcome = True
		else:
			outcome = False

		return outcome


	def isontorrent(self, torrentid):

		if (self.context == "ALL") or (self.context == torrentid):
			outcome = True
		else:
			outcome = False

		return outcome




