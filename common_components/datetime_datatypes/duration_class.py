from . import duration_privatefunctions as DurationFunction

# ===========================================================================================================
# This class captures all datetime-durations in seconds.
# ===========================================================================================================


class DefineDuration:

	def __init__(self):

		# The length of the duration in seconds, as an integer
		self.dvalue = 0



# ===========================================================================================================
# Basic Value Setters
# ===========================================================================================================

# ---------------------------------------------------------
# Sets the duration using a Value-Unit pair of integers
# ---------------------------------------------------------

	def setfromvalues(self, dvalue, dunit):

		if DurationFunction.isdurationunitvalid(dunit) == True:
			self.dvalue = DurationFunction.convertunit(dvalue, dunit, "Seconds")
		else:
			self.dvalue = 0
			print("Invalid Unit - ", dunit)



	# ---------------------------------------------------------
	# Sets the duration using an existing duration (object)
	# ---------------------------------------------------------

	def setfromobject(self, existingduration):

		self.dvalue = existingduration.dvalue



# ===========================================================================================================
# Object Processing
# ===========================================================================================================




# ===========================================================================================================
# Get Information
# ===========================================================================================================


# ---------------------------------------------------------
# Returns the duration in seconds
# ---------------------------------------------------------

	def getsecondsvalue(self):

		return self.dvalue



# ---------------------------------------------------------
# Returns the duration in Seconds, Days or Months
# ---------------------------------------------------------

	def getvalue(self, unitlabel):

		if DurationFunction.isdurationunitvalid(unitlabel) == True:
			outcome = DurationFunction.convertunit(self.dvalue, "Seconds", unitlabel)
		else:
			outcome = 0
			print("Invalid Unit - ", unitlabel)
		return outcome



# ---------------------------------------------------------
# Adjusts the duration
# ---------------------------------------------------------

	def adjustduration(self, adjustmentduration):

		self.setfromvalues(self.dvalue + adjustmentduration.dvalue, "Seconds")


