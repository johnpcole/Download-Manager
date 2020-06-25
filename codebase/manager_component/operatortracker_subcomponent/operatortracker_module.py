from . import operatortracker_class as OperatorTrackerClass



def createtracker(operatorqueuelocation, sessiondataqueuelocation):
	return OperatorTrackerClass.DefineOperatorTracker(operatorqueuelocation, sessiondataqueuelocation)

