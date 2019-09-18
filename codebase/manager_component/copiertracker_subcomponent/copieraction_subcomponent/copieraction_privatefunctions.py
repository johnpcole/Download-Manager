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
	columncount = 0

	if "Source File" in results.keys():
		outcome.append("Downloaded File")
		outcome.append("(On Downloads drive)")
		outcome.extend(rendercopyresultdetail(results["Source File"]))
		columncount = columncount + 1

	if "Existing File" in results.keys():
		if statusenum.get("Succeeded") == True:
			outcome.append("Pre-existing File which was overwritten")
		elif statusenum.get("Confirm") == True:
			outcome.append("Pre-existing File which will be overwritten if confirmed")
		else:
			outcome.append("Pre-existing File which would have been overwritten")
		outcome.append("(On Videos drive)")
		outcome.extend(rendercopyresultdetail(results["Existing File"]))
		columncount = columncount + 1

	if "New Copied File" in results.keys():
		outcome.append("Downloaded File")
		outcome.append("(On Downloads drive)")
		outcome.extend(rendercopyresultdetail(results["New Copied File"]))
		columncount = columncount + 1

	if "Error" in results.keys():
		outcome.append("File not copied!")
		outcome.append("(Error encountered)")
		outcome.extend(results["Error"])
		outcome.extend("")
		columncount = columncount + 1

	realoutcome = {"filepath": sanitisetargetpath(targetpath)}

	newoutcome = []
	for rowval in range(0, 4):
		for colval in range(0, columncount+1):
			newoutcome.append(outcome[(rowval * (columncount+1)) + colval])
	realoutcome["outcomes"] = newoutcome

	return realoutcome


def rendercopyresultdetail(filedetails):

	outcome = []
	outcome.append(DataConversion.sanitisesize(filedetails["filesize"]))
	datetime = sanitisecopydatetimestamp(filedetails["datetime"] + "000")
	outcome.append(datetime[:-3])
	return outcome




