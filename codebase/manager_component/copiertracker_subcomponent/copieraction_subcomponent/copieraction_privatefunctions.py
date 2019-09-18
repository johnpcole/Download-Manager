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

	titles = []
	subtitles = []
	sizes = []
	datetimes = []

	if "Source File" in results.keys():
		titles.append("Downloaded File")
		subtitles.append("(On Downloads drive)")
		sizes.append(rendercopysize(results["Source File"]))
		datetimes.append(rendercopydatetime(results["Source File"]))

	if "Existing File" in results.keys():
		if statusenum.get("Succeeded") == True:
			titles.append("Pre-existing File which was overwritten")
		elif statusenum.get("Confirm") == True:
			titles.append("Pre-existing File which will be overwritten if confirmed")
		else:
			titles.append("Pre-existing File which would have been overwritten")
		subtitles.append("(On Videos drive)")
		sizes.append(rendercopysize(results["Existing File"]))
		datetimes.append(rendercopydatetime(results["Existing File"]))

	if "New Copied File" in results.keys():
		titles.append("Downloaded File")
		subtitles.append("(On Downloads drive)")
		sizes.append(rendercopysize(results["New Copied File"]))
		datetimes.append(rendercopydatetime(results["New Copied File"]))

	if "Error" in results.keys():
		titles.append("File not copied!")
		subtitles.append("(Error encountered)")
		sizes.extend(results["Error"])
		datetimes.extend("")

	realoutcome = {"filepath": sanitisetargetpath(targetpath), "outcomes": [titles, subtitles, sizes, datetimes]}

	return realoutcome


def rendercopysize(filedetails):

	return DataConversion.sanitisesize(filedetails["filesize"])


def rendercopydatetime(filedetails):

	datetime = sanitisecopydatetimestamp(filedetails["datetime"] + "000")
	return datetime[:-3]










