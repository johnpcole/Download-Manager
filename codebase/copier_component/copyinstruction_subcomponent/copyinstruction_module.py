from . import copyinstruction_class as CopyInstructionClass


def createinstruction():
	return CopyInstructionClass.DefineInstruction()


def isalldone(newinstructionset):
	if newinstructionset['action'] == "Null":
		outcome = True
	else:
		outcome = False
	return outcome

def isfolderrefresh(newinstructionset):
	if newinstructionset['action'] == "Scrape TV Shows":
		outcome = True
	else:
		outcome = False
	return outcome

def isvalidinstruction(newinstructionset):

	if isinstance(newinstructionset, dict):
		outcome = True
		if "copyid" not in newinstructionset.keys():
			outcome = False
		if "action" not in newinstructionset.keys():
			outcome = False
		else:
			if newinstructionset['action'] == "File Copy":
				if "source" not in newinstructionset.keys():
					outcome = False
				if "target" not in newinstructionset.keys():
					outcome = False
				if "overwrite" not in newinstructionset.keys():
					outcome = False
	else:
		outcome = False

	if outcome is False:
		print("Invalid response from Download-Manager:")
		print(newinstructionset)
		print("====================================")
	return outcome

