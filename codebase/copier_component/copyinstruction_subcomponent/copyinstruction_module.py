from . import copyinstruction_class as CopyInstructionClass


def createinstruction():
	return CopyInstructionClass.DefineInstruction()


def isalldone(copyid):
	if copyid == "00000000000000000":
		outcome = True
	else:
		outcome = False
	return outcome

def isfolderrefresh(copyid):
	if copyid == "-----------------":
		outcome = True
	else:
		outcome = False
	return outcome

