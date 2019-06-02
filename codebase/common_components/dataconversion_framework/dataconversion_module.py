import operator as Operators



# =========================================================================================
# Sorts a dictionary by the specified sort attribute
# =========================================================================================

def sortdictionary(rawdictionary, sortattribute, reverseflag):

	outcome = sorted(rawdictionary, key=Operators.attrgetter(sortattribute), reverse=reverseflag)

	return outcome



# =========================================================================================
# Converts a numeric value of bytes into a string using SI units
# =========================================================================================

def sanitisesize(rawsize):

	if rawsize > 1000000000:
		outcome = ("%8.2f" % (int(rawsize / 10000000) * 0.01)) + " Gb"
	elif rawsize > 1000000:
		outcome = ("%8.2f" % (int(rawsize / 10000) * 0.01)) + " Mb"
	elif rawsize > 1000:
		outcome = ("%8.2f" % (int(rawsize / 10) * 0.01)) + " kb"
	else:
		outcome = str(int(rawsize)) + " b"

	return outcome



# =========================================================================================
# Converts a numeric value of seconds into a string using s/m/h/d units
# =========================================================================================

def sanitisetime(rawtime):

	if rawtime > 86400:
		outcome = ("%8.1f" % (int(rawtime / 8640) * 0.1)) + " d"
	elif rawtime > 3600:
		outcome = ("%8.1f" % (int(rawtime / 360) * 0.1)) + " h"
	elif rawtime > 60:
		outcome = ("%8.1f" % (int(rawtime / 6) * 0.1)) + " m"
	elif rawtime > 1:
		outcome = str(rawtime) + "s"
	else:
		outcome = "-"

	return outcome



# =========================================================================================
# Converts non-alphanumeric characters into underscores
# =========================================================================================

def sanitisetext(rawtext):

	outcome = ""

	stringsize = len(rawtext)

	if stringsize > 0:

		if rawtext.isalnum() == True:
			outcome = rawtext

		else:

			for index in range(0, stringsize, 1):
				charitem = rawtext[index:index+1]
				charval = ord(charitem)

				if (charval >= 48) and (charval <= 57):
					outcome = outcome + charitem
				elif (charval >= 65) and (charval <= 90):
					outcome = outcome + charitem
				elif (charval >= 97) and (charval <= 122):
					outcome = outcome + charitem
				elif charval == 46:
					outcome = outcome + charitem
				else:
					outcome = outcome + "_"

	return outcome



# =========================================================================================
# Returns a string providing the season shorthand s00, s01 etc
# =========================================================================================

def minifyseason(seasonname, episodename):

	episodesplit = episodename.split(" ")

	if episodesplit[0] == "Special":
		outcome = "s00"
	else:
		seasonsplit = seasonname.split(" ")
		if seasonsplit[0] == "Season":
			s = "00" + seasonsplit[1]
			outcome = "s" + s[-2:]
		elif seasonname[:7] == "Special":
			outcome = "s00"
		else:
			outcome = "-"

	return outcome



# =========================================================================================
# Returns a string providing the episode shorthand e01, e02, e01e02 etc
# =========================================================================================

def minifyepisode(episodename):

	episodesplit = episodename.split(" ")
	if len(episodesplit) > 1:
		if episodesplit[0] == "Ep.":
			f = "00" + episodesplit[1]
			f = "e" + f[-2:]
			g = "00" + episodesplit[3]
			g = "e" + g[-2:]
			e = f + g
		else:
			e = "00" + episodesplit[1]
			e = "e" + e[-2:]
	else:
		e = episodename
	return e


# =========================================================================================
# Returns the lead character of a name a, b, c etc - Ignoring initial The, A or An
# =========================================================================================

def getinitial(name):

	namesplit = name.split(" ")
	if len(namesplit) > 1:
		firstword = namesplit[0]
		firstword = firstword.lower()
		if (firstword == "the") or (firstword == "a") or (firstword == "an"):
			noun = namesplit[1]
		else:
			noun = namesplit[0]
	else:
		noun = name
	outcome = noun[:1]
	if (outcome == "1") or (outcome == "2") or (outcome == "3") or (outcome == "4") or (outcome == "5"):
		outcome = "0"
	elif (outcome == "6") or (outcome == "7") or (outcome == "8") or (outcome == "9") or (outcome == "#"):
		outcome = "0"
	elif (outcome == "!") or (outcome == "$") or (outcome == "%") or (outcome == "#") or (outcome == "@"):
		outcome = "0"

	return outcome.upper()



def dearticle(realname):
	name = realname.lower()
	splittest = name.split(" ")
	if splittest[0] == "the":
		outcome = realname[4:] + "|||The"
	elif splittest[0] == "a":
		outcome = realname[2:] + "|||A"
	elif splittest[0] == "an":
		outcome = realname[3:] + "|||An"
	else:
		outcome = realname + "|||x"
	return outcome


def rearticle(switchedname):
	splittext = switchedname.split("|||")
	if splittext[0] == "x":
		outcome = switchedname
	else:
		outcome = splittext[1] + " " + splittext[0]
	return outcome



