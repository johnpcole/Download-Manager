from ....common_components.dataconversion_framework import dataconversion_module as DataConversion
from ....common_components.datetime_datatypes import datetime_module as DateTime
from ....common_components.filesystem_framework import filesystem_module as FileSystem


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

	datetime = actionid[:4] + "-" + actionid[5:7] + "-" + actionid[8:10] + " "
	datetime = datetime + actionid[11:13] + ":" + actionid[14:16] + ":" + actionid[17:19]
	datetime = datetime + " [" + actionid[20:] + "]"

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
		titles.append("Pre-existing File")
		subtitles.append("(On Videos drive)")
		sizes.append(rendercopysize(results["Existing File"]))
		datetimes.append(rendercopydatetime(results["Existing File"]))

	if "New Copied File" in results.keys():
		titles.append("Copied File")
		subtitles.append("(On Videos drive)")
		sizes.append(rendercopysize(results["New Copied File"]))
		datetimes.append(rendercopydatetime(results["New Copied File"]))

	if "Error" in results.keys():
		titles.append("File not copied!")
		subtitles.append("(Error encountered)")
		sizes.append(results["Error"])
		datetimes.append("")

	if "Existing File" in results.keys():
		if statusenum.get("Succeeded") == True:
			description = "The pre-existing file was overwritten with the downloaded file"
		elif statusenum.get("Confirm") == True:
			description = "The pre-existing file will be overwritten if you confirm this copy action"
		else:
			description = "The pre-existing file may have been compromised by the failed copy action"
	else:
		if statusenum.get("Succeeded") == True:
			description = "The downloaded file was successfully copied"
		else:
			description = "The downloaded file was <b>NOT</b> successfully copied"

	realoutcome = {"filepath": sanitisetargetpath(targetpath), "outcomes": [titles, subtitles, sizes, datetimes],
																						"description" : description}

	return realoutcome


def rendercopysize(filedetails):

	return DataConversion.sanitisesize(filedetails["filesize"])


def rendercopydatetime(filedetails):

	datetime = sanitisecopydatetimestamp(filedetails["datetime"] + "000")
	return datetime[:-6]





# =========================================================================================

def generatesavedatafilename(filelocation):

	currentdatetime = DateTime.getnow()
	currentdatetimetext = currentdatetime.getiso()
	currentdatetimeprefix = currentdatetimetext[:4] + "_" + currentdatetimetext[4:6] + "_" + currentdatetimetext[6:8] + "_"
	currentdatetimeprefix = currentdatetimeprefix + currentdatetimetext[8:10] + "_" + currentdatetimetext[10:12] + "_" + currentdatetimetext[12:14]
	foundgap = ""
	for currentsearch in range(0, 1000, 1):
		if foundgap == "":
			indexstring = "0000" + str(currentsearch)
			trialfilename = currentdatetimeprefix + "_" + indexstring[-3:]
			trialfile = generatesavedatafullpath(filelocation, trialfilename)
			if FileSystem.doesexist(trialfile) is False:
				foundgap = trialfilename

	if foundgap == "":
		print("Could not find unique copier action save slot for " + currentdatetimetext + " in " + filelocation)
		foundgap = generatesavedatafilename(filelocation)

	return foundgap


def generatesavedatafullpath(filelocation, filename):

	outcome = FileSystem.concatenatepaths(filelocation, filename + ".action")
	return outcome



