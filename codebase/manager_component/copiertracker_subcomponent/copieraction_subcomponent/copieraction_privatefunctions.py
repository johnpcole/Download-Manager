from ....common_components.dataconversion_framework import dataconversion_module as DataConversion
from ....common_components.datetime_datatypes import datetime_module as DateTime

def sanitisestatus(statuslabel):

	if statuslabel == "In Progress":
		outcome = "InProgress"
	else:
		outcome = statuslabel

	return outcome.lower()




def sanitisetargetpath(rawpath):

	target = rawpath
	target = target.replace("/", " / ")
	return target[1:]




def sanitisecopydatetimestamp(actionid):

	datetime = actionid[:4] + "-" + actionid[4:6] + "-" + actionid[6:8] + " "
	datetime = datetime + actionid[8:10] + ":" + actionid[10:12] + ":" + actionid[12:14]
	datetime = datetime + " [" + actionid[14:] + "]"

	return datetime


def rendercopyresults(results, statusenum, targetpath):

	outcome = []

	outcome.append(sanitisetargetpath(targetpath))

	if "Source File" in results.keys():
		outcome.append("Downloaded File:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small>(On Downloads drive)</small>")
		outcome.extend(results["Source File"])
	if "Existing File" in results.keys():
		if statusenum.get("Succeeded") == True:
			outcome.append("Pre-existing File which was overwritten:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small>(On Videos drive)</small>")
		elif statusenum.get("Confirm") == True:
			outcome.append("Pre-existing File which will be overwritten if confirmed:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small>(On Videos drive)</small>")
		else:
			outcome.append("Pre-existing File which would have been overwritten:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small>(On Videos drive)</small>")

		outcome.extend(results["Existing File"])
	if "New Copied File" in results.keys():
		outcome.append("Copied File:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small>(On Videos drive)</small>")
		outcome.extend(results["New Copied File"])
	if "Error" in results.keys():
		outcome.append("File not copied; Error encountered:")
		outcome.extend(results["Error"])
	return outcome


def rendercopyresultdetail(filedetails):

	outcome = []
	outcome.append("File size = " + DataConversion.sanitisesize(filedetails["filesize"]))
	datetime = sanitisecopydatetimestamp(filedetails["datetime"] + "000")
	outcome.append("File time = " + datetime[:-3])
	return outcome




