import sys, os
from time import sleep

BLACKBOARD = {"BATTERY_LEVEL": 100,
			  "SPOT": True,
			  "GENERAL": True,
			  "DUSTY_SPOT": True,
			  "HOME_PATH": [0, 1, 2, 3]}

class Roomba():
	def __init__(self):
		while(True):
			self.battery_1()
			self.spot_check()
			self.clean_until_fail()

	def battery_1(self):
		if(BLACKBOARD["BATTERY_LEVEL"] < 30):
			BLACKBOARD["HOME_PATH"] = [0, 1, 2, 3]
			print("Home Path Set")
			print("Going Home")
			print("Docking")
			exit(1)

	def spot_check(self):
		if(BLACKBOARD["SPOT"]):
			for i in range(20):
				# sleep(1)
				if(i % 5 == 0):
					print("Cleaning Spot " + str(100 * i / 20) + "%")
			print("Cleaning Spot 100%")
			BLACKBOARD["SPOT"] = False

	def clean_until_fail(self):
		if(BLACKBOARD["GENERAL"]):
			while(BLACKBOARD["BATTERY_LEVEL"] >= 30):
				if(BLACKBOARD["DUSTY_SPOT"]):
					for i in range(35):
						# sleep(1)
						if(i % 5 == 0):
							print("Cleaning Dusty Spot " + str(100 * i / 35) + "%")
					print("Cleaning Dusty Spot 100%")
					BLACKBOARD["DUSTY_SPOT"] = False
				BLACKBOARD["BATTERY_LEVEL"] -= 5
				print("Battery: " + str(BLACKBOARD["BATTERY_LEVEL"]))
			BLACKBOARD["GENERAL"] = False


def main():
	cleaner = Roomba()


if __name__ == '__main__':
	main()