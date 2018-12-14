import sys, os
from time import sleep

BLACKBOARD = {"BATTERY_LEVEL": 100,
			  "SPOT": True,
			  "GENERAL": True,
			  "DUSTY_SPOT": True,
			  "HOME_PATH": [0, 1, 2, 3]}

class Roomba():
	print("\033[1m======== Initializing Roomba ========\033[0m\n")
	def __init__(self):
		while(True):
			self.battery_1()
			self.spot_check()
			self.clean_until_fail()

	def battery_1(self):
		if(BLACKBOARD["BATTERY_LEVEL"] < 30):
			BLACKBOARD["HOME_PATH"] = [0, 1, 2, 3]
			print("Find Home               . . .   \033[1mSUCCEEDED\033[0m")
			print("Go Home                 . . .   \033[1mSUCCEEDED\033[0m")
			print("Docking                 . . .   \033[1mSUCCEEDED\033[0m")
			print("\n\033[1m======== Roomba Powering Down ========\033[0m")
			exit(1)

	def spot_check(self):
		if(BLACKBOARD["SPOT"]):
			for i in range(20):
				# sleep(1)
				if(i % 5 == 0):
					print("Spot Cleaning           . . .   RUNNING (%d%%)" % (100 * i / 20))
			print("Spot Cleaning           . . .   \033[1mSUCCEEDED\033[0m\n")
			BLACKBOARD["SPOT"] = False
		else:
			print("Spot                    . . .   \033[1mFAILED\033[0m")

	def clean_until_fail(self):
		if(BLACKBOARD["GENERAL"]):
			print("General Cleaning        . . .   RUNNING")
			while(BLACKBOARD["BATTERY_LEVEL"] >= 30):
				if(BLACKBOARD["DUSTY_SPOT"]):
					for i in range(35):
						# sleep(1)
						if(i % 5 == 0):
							print("Dusty Spot Cleaning     . . .   RUNNING (" + str(100 * i / 35) + "%)")
					print("Dusty Spot Cleaning     . . .   \033[1mSUCCEEDED\033[0m\n")
					BLACKBOARD["DUSTY_SPOT"] = False
				print("General Cleaning        . . .   \033[1mSUCCEEDED\033[0m [Battery: %d%%]" % BLACKBOARD["BATTERY_LEVEL"])
				BLACKBOARD["BATTERY_LEVEL"] -= 5
			print("General                 . . .   \033[1mSUCCEEDED\033[0m\n")
			BLACKBOARD["GENERAL"] = False
		else:
			print("General Cleaning       . . .   \033[1mFAILED\033[0m")


def main():
	cleaner = Roomba()


if __name__ == '__main__':
	main()