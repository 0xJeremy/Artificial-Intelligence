import sys, os
from time import sleep

BLACKBOARD = {"BATTERY_LEVEL": 100,
			  "SPOT": True,
			  "GENERAL": True,
			  "DUSTY_SPOT": True,
			  "HOME_PATH": "PATH_TO_DOCKING_STATION"}

def sprint(operation, state, battery):
	operation = operation.ljust(24)
	print(operation, end = '\r')
	sleep(0.3)
	print(operation + ".", end = '\r')
	sleep(0.3)
	print(operation + ". .", end = '\r')
	sleep(0.3)
	print(operation + ". . .", end = '\r')
	sleep(0.3)
	if(battery):
		print(operation + ". . .   \033[1m" + state + "\033[0m [Battery: %d%%]" % BLACKBOARD["BATTERY_LEVEL"])
	else:
		print(operation + ". . .   \033[1m" + state + "\033[0m")

class Roomba():
	def __init__(self):
		print("\033[1m======== Initializing Roomba ========\033[0m\n")
		while(True):
			self.battery_1()
			self.spot_check()
			self.clean_until_fail()

	def battery_1(self):
		if(BLACKBOARD["BATTERY_LEVEL"] < 30):
			sprint("Find Home", "SUCCEEDED", False)
			sprint("Go Home", "SUCCEEDED", False)
			sprint("Docking", "SUCCEEDED", False)
			BLACKBOARD["BATTERY_LEVEL"] = 100

	def spot_check(self):
		if(BLACKBOARD["SPOT"]):
			for i in range(20):
				# sleep(1)
				if(i % 5 == 0):
					print("Spot Cleaning           . . .   RUNNING (%2d%%)" % (100 * i / 20))
			sprint("Spot Cleaning", "SUCCEEDED", False)
			BLACKBOARD["BATTERY_LEVEL"] -= 5
			BLACKBOARD["SPOT"] = False
		else:
			sprint("Spot", "FAILED", False)

	def clean_until_fail(self):
		if(BLACKBOARD["GENERAL"]):
			sprint("General Cleaning", "RUNNING", False)
			while(BLACKBOARD["BATTERY_LEVEL"] >= 30):
				if(BLACKBOARD["DUSTY_SPOT"]):
					for i in range(35):
						sleep(1)
						if(i % 5 == 0):
							print("Dusty Spot Cleaning     . . .   RUNNING (%2d%%)" % (100 * i / 35))
						BLACKBOARD["BATTERY_LEVEL"] -= 1
					sprint("Dusty Spot CLeaning", "SUCCEEDED", False)
					BLACKBOARD["DUSTY_SPOT"] = False
				# print("General Cleaning        . . .   \033[1mSUCCEEDED\033[0m [Battery: %d%%]" % BLACKBOARD["BATTERY_LEVEL"])
				BLACKBOARD["BATTERY_LEVEL"] -= 5
				sprint("General", "SUCCEEDED", True)
			BLACKBOARD["GENERAL"] = False
		else:
			sprint("General Cleaning", "FAILED", False)


def main():
	cleaner = Roomba()


if __name__ == '__main__':
	main()