import math, sys, os
from Queue import *
import networkx as nx
import heapq
import copy

NUM_PANCAKES = 5

class pQueue:
	def __init__(self):
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, element, priority):
		heapq.heappush(self.elements, (priority, element))

	def get(self):
		return heapq.heappop(self.elements)[1]

class Pancakes:
	def __init__(self, stack, back_cost):
		self.stack = stack
		self.back_cost = back_cost
		self.size = len(stack)-1
		self.forward_cost = self.heuristic()
		self.total_cost = self.back_cost + self.forward_cost

	def check_order(self):
		for x in range(self.size):
			if(pancakes.stack[x] < pancakes.stack[x+1]):
				return False
		return True

	def heuristic(self):
		cost = 0
		print("LENGTH: " + str(range(self.size)))
		for x in range(self.size):
			diff = abs(self.stack[x] - self.stack[x+1])
			if(diff > 1):
				cost += 1
		return cost

	def flip(self, location):
		location -= 1
		temp, x = 0, 0
		while(x < location):
			temp = self.stack[x]
			self.stack[x] = self.stack[location]
			self.stack[location] = temp
			x += 1
			location -= 1

def astar(pancakes):
	open_list = pQueue()
	open_list.put(pancakes, pancakes.total_cost)

	closed_list = set()

	G = nx.Graph()
	G.add_node(pancakes)

	while(not open_list.empty()):
		current = open_list.get()
		closed_list.add(current)

		for x in range(current.size):
			temp = copy.deepcopy(pancakes)
			temp.back_cost += 1
			temp.flip(x)
			if(current.check_order):
				break
			if(temp in closed_list):
				continue
			G.add_node(temp)
			G.add_edge(current, temp)

	return closed_list



	# open_list = Queue(maxsize=0)
	# closed_list = Queue(maxsize=0)
	# G = nx.Graph()

	# G.add_node(pancakes)
	# open_list.put(pancakes)

	# while(!open_list.empty()):
	# 	current = open_list.get()

	# 	if(current.check_order):
	# 		return current

	# 	for x in range(len(current.size)):
	# 		temp = copy.deepcopy(p)
	# 		temp.back_cost += 1
	# 		temp.flip(x)
	# 		G.add_node(temp)
	# 		G.add_edge(current, temp)


def main():
	stack = [3, 2, 5, 1, 6, 4, 7]
	p = Pancakes(stack, 0)
	print("EXPECTED: 5")
	print("          " + str(p.forward_cost))
	closed_list = astar(p)
	for i in closed_list:
		print(i)


if __name__=='__main__':
	main()