import sys, os
from time import sleep
import random

#********************************************************************
#						Initial Parameters
#********************************************************************

BLACKBOARD = {"BATTERY_LEVEL": 100,
			  "SPOT": True,
			  "GENERAL": True,
			  "DUSTY_SPOT": True,
			  "HOME_PATH": "PATH_TO_DOCKING_STATION"}

#********************************************************************
#						Helper Functions
#********************************************************************

def randomize_environment():
	BLACKBOARD["SPOT"] = bool(random.getrandbits(1))
	BLACKBOARD["GENERAL"] = bool(random.getrandbits(1))
	BLACKBOARD["DUSTY_SPOT"] = bool(random.getrandbits(1))

def sprint(operation, state, battery):
	operation = operation.ljust(24)
	print(operation, end = '\r')
	for i in range(3):
		sleep(0.3)
		operation += ". "
		print(operation, end = '\r')
	sleep(0.3)
	if(battery):
		print(operation + "  \033[1m" + state + "\033[0m [Battery: %d%%]" % BLACKBOARD["BATTERY_LEVEL"])
	else:
		print(operation + "  \033[1m" + state + "\033[0m")

def running(operation, time):
	operation = operation.ljust(24)
	for i in range(time):
		sleep(1)
		BLACKBOARD["BATTERY_LEVEL"] -= 1
		if(i % 5 == 0):
			print(operation + ". . .   RUNNING (%2d%%)" % (100 * i / time))

#********************************************************************
#						Roomba Class
#********************************************************************

class Roomba():
	def __init__(self):
		print("\033[1m======== Initializing Roomba ========\033[0m\n")
		while(True):
			self.battery_1()
			self.spot_check()
			self.clean_until_fail()
			randomize_environment()

	def battery_1(self):
		if(BLACKBOARD["BATTERY_LEVEL"] < 30):
			sprint("Find Home", "SUCCEEDED", False)
			BLACKBOARD["HOME_PATH"] = "PATH_TO_DOCKING_STATION"
			sprint("Go Home", "SUCCEEDED", False)
			sprint("Docking", "SUCCEEDED", False)
			print()
			BLACKBOARD["BATTERY_LEVEL"] = random.randint(80, 100)

	def spot_check(self):
		if(BLACKBOARD["SPOT"]):
			running("Spot Cleaning", 20)
			sprint("Spot Cleaning", "SUCCEEDED", False)
			print()
			BLACKBOARD["SPOT"] = False
		else:
			sprint("Spot", "FAILED", False)
			print()

	def clean_until_fail(self):
		if(BLACKBOARD["GENERAL"]):
			print("General Cleaning        . . .   RUNNING")
			while(BLACKBOARD["BATTERY_LEVEL"] >= 30):
				if(BLACKBOARD["DUSTY_SPOT"]):
					running("Dusty Spot Cleaning", 35)
					sprint("Dusty Spot CLeaning", "SUCCEEDED", False)
					print()
					BLACKBOARD["DUSTY_SPOT"] = False
				BLACKBOARD["BATTERY_LEVEL"] -= random.randint(1, 10)
				sprint("General Cleaning", "SUCCEEDED", True)
			BLACKBOARD["GENERAL"] = False
		else:
			sprint("General Cleaning", "FAILED", False)
			print()

#********************************************************************
#						Main Function
#********************************************************************

def main():
	cleaner = Roomba()


if __name__ == '__main__':
	main()