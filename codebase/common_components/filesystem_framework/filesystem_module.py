import os as OperatingSystem
from ...common_components.logging_framework import logging_module as Logging


def mountnetworkdrive(mountpoint, networkpath, username, password, reason):
	Logging.printout("- Connecting to File-Server&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small>(" + reason + ")</small>")

	if concatenatepaths(" ", " ") == " / ":
		outcome = OperatingSystem.system('sudo mount -t cifs -o username='+username+',password='+password+',uid=pi,gid=pi,noexec,vers=2.0 '+networkpath+' '+mountpoint)
	else:
		if username != "":
			outcome = OperatingSystem.system('NET USE '+mountpoint+' '+networkpath+' '+password+' '+'/USER:'+username+' /PERSISTENT:NO')
		else:
			outcome = OperatingSystem.system('NET USE '+mountpoint+' '+networkpath)
	return outcome




def unmountnetworkdrive(mountpoint):
	Logging.printout("- Disconnecting File-Server")

	if concatenatepaths(" ", " ") == " / ":
		outcome = OperatingSystem.system('sudo umount '+mountpoint)
	else:
		outcome = OperatingSystem.system('NET USE '+mountpoint+' /DELETE')
	return outcome

# ---------------------------------------------
# Reads a file from disk and returns a list,
# where each list item is a line in the file
# ---------------------------------------------

def readfromdisk(filename):
	newfilelist = []

	try:
		# Open the file for the duration of this process
		with open(filename, 'r') as fileobject:

			# Loop over all lines in the file
			for fileline in fileobject.readlines():

				# Only process if the line isn't blank
				if fileline != "":
					newfilelist.append(fileline.rstrip('\r\n'))

	except:
		# Print an error if the file cannot be read
		Logging.printout("Cannot read file - " + filename)

	return newfilelist



# ---------------------------------------------
# Returns a list of strings, extracted from a
# single string of tab separated substrings
# ---------------------------------------------

def extracttabulateddata(fileline):
	splitdata = fileline.split("\t")
	return splitdata



# ---------------------------------------------
# Returns a list of strings, extracted from a
# single string of comma-space separated substrings
# ---------------------------------------------

def extractcommadata(fileline):
	splitdata = fileline.split(", ")
	return splitdata



# ---------------------------------------------
# Returns a list of two strings, extracted from a
# single string of space-equals-space separated substrings
# ---------------------------------------------

def extractdatapair(dataitem):
	splitdata = dataitem.split(" = ")
	return splitdata[0], splitdata[1]



# ---------------------------------------------
# Returns a list items found in the specified
# folderpath, with File/Folder/Unknown designations
# ---------------------------------------------

def getfolderlisting(folderpath):
	outcome = {}

	try:
		listing = OperatingSystem.listdir(folderpath)

		for listitem in listing:
			fullitempath = OperatingSystem.path.join(folderpath, listitem)
			if OperatingSystem.path.isfile(fullitempath) == True:
				itemtype = "File"
			elif OperatingSystem.path.isdir(fullitempath) == True:
				itemtype = "Folder"
			else:
				itemtype = "Unknown"
			outcome[listitem] = itemtype

	except:
		Logging.printout("Cannot access folder - " + folderpath)

	return outcome



# ---------------------------------------------
# Returns a path based on a root and a subitem
# ---------------------------------------------

def concatenatepaths(path1, path2):

	suffix = path2
	if path2 != "":
		if path2[0:1] == "/":
			suffix = path2[1:]
	if path1 == "":
		prefix = " "
		outcome = OperatingSystem.path.join(prefix, suffix)
		outcome = outcome[1:]
	else:
		prefix = path1
		if len(path1) == 2:
			if path1[1:2] == ":":
				prefix = path1 + "\\"
		outcome = OperatingSystem.path.join(prefix, suffix)

	return outcome



# ---------------------------------------------
# Returns whether a path (file or folder) exists
# ---------------------------------------------

def doesexist(fullpath):
	return OperatingSystem.path.exists(fullpath)



# ---------------------------------------------
# Returns a file's extension
# ---------------------------------------------

def getextension(filename):
	if "." in filename:
		filenamesplit = filename.split(".")
		outcome = filenamesplit[len(filenamesplit) - 1]
	else:
		outcome = ""

	return outcome



# ---------------------------------------------
# Returns a file's name
# ---------------------------------------------

def getname(filename):
	extension = getextension(filename)

	if extension == "":
		if filename[-1:] == ".":
			outcome = filename[:-1]
		else:
			outcome = filename
	else:
		extensionlength = 0 - len(extension) - 1
		outcome = filename[:extensionlength]

	return outcome



# ---------------------------------------------
# Writes a file to disk from a list
# ---------------------------------------------

def writetodisk(filename, outputlist, appendwritemode):

	if appendwritemode == "Overwrite":
		modeflag = 'w'
	elif appendwritemode == "Append":
		modeflag = 'a'
	else:
		assert 1 == 0, ("Unknown file write output mode: " + appendwritemode)

	newlist = []
	for originalitem in outputlist:
		newlist.append(originalitem)
		newlist.append("\n")

	try:
		# Open the file for the duration of this process
		with open(filename, modeflag) as targetfile:

			# Print out all items in list
			targetfile.writelines(newlist)

	except:
		# Print an error if the file cannot be written
		Logging.printout("Cannot write file - " + filename)



# ---------------------------------------------
# Returns a path based on a list of subfolders
# ---------------------------------------------

def createpathfromlist(pathlist):

	outcome = ""
	for pathitem in pathlist:
		outcome = concatenatepaths(outcome, pathitem)

	return outcome



# ---------------------------------------------
# Copies a file
# ---------------------------------------------

def copyfile(source, target):
	space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
	arrows = space + space + "&darr;"
	indent = space + space + space + space + space
	lineofarrows = arrows + arrows + arrows + arrows + arrows
	Logging.printout("Copying File:&nbsp;" + space + source + "</br>" + indent + lineofarrows + "</br>" + indent + target)

	if concatenatepaths(" ", " ") == " / ":
		outcome = OperatingSystem.system('cp "' + source + '" "' + target + '"')
	else:
		outcome = OperatingSystem.system('copy "' + source + '" "' + target + '"')

	return outcome

