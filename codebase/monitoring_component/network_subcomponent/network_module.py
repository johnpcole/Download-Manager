import os as OperatingSystem


def getvpnstatus():

	result = OperatingSystem.popen('ifconfig').readline()
	outcome = 0
	for logrow in result:
		if logrow.find("<UP,") > 0:
			splitdata = logrow.split(": flags=")
			if splitdata[0] == "tun0":
				outcome = 1
	print("checked vpn status: ", outcome)
	return outcome

