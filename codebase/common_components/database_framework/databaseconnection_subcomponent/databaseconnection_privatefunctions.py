from ...datetime_datatypes import datetime_module as DateTime


def waittoaccess(turn):

	if turn != 0:
		go = False
		while go == False:
			timefraction = DateTime.getnowfraction(False)
			if (timefraction >= 0) and (timefraction <= 40) and (turn == 1):
				go = True
			elif (timefraction >= 50) and (timefraction <= 90) and (turn == 2):
				go = True
			#elif (timefraction >= 0) and (timefraction <= 23) and (turn == 11):
			#	go = True
			#elif (timefraction >= 33) and (timefraction <= 56) and (turn == 12):
			#	go = True
			#elif (timefraction >= 66) and (timefraction <= 90) and (turn == 13):
			#	go = True
			#elif (timefraction >= 0) and (timefraction <= 15) and (turn == 21):
			#	go = True
			#elif (timefraction >= 25) and (timefraction <= 40) and (turn == 22):
			#	go = True
			#elif (timefraction >= 50) and (timefraction <= 65) and (turn == 23):
			#	go = True
			#elif (timefraction >= 75) and (timefraction <= 90) and (turn == 24):
			#	go = True

	return 0


