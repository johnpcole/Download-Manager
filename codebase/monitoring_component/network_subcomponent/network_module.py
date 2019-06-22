import os as OperatingSystem


def getvpnstatus():

	result = OperatingSystem.popen('ifconfig')
	outcome = 0
	for logrow in result.readlines():
		print(logrow)
		if logrow.find("<UP,") > 0:
			splitdata = logrow.split(": flags=")
			if splitdata[0] == "tun0":
				outcome = 1
	return outcome

