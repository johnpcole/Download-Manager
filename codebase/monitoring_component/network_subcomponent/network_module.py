import os as OperatingSystem


def getvpnstatus():

	result = OperatingSystem.popen('ifconfig').readline()
	outcome = False
	for logrow in result:
		if logrow.find("<UP,") > 0:
			splitdata = logrow.split(": flags=")
			if splitdata[0] == "tun0":
				outcome = True
	return outcome

