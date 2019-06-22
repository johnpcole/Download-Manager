import os as OperatingSystem


def getvpnstatus():

	result = OperatingSystem.popen('ifconfig')
	print("<><><><><><><><><><><><><><><><><><><><><><><><>")
	print(result)
	print("<><><><><><><><><><><><><><><><><><><><><><><><>")
	outcome = 0
	for logrow in result.readlines():
		print(logrow)
		if logrow.find("<UP,") > 0:
			splitdata = logrow.split(": flags=")
			if splitdata[0] == "tun0":
				outcome = 1
				print("Found it")
	print("checked vpn status: ", outcome)
	return outcome

