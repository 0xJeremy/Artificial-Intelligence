import math, sys, os
from Queue import *
import networkx as nx
import heapq
import copy

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
			if(self.stack[x] > self.stack[x+1]):
				return False
		return True

	def heuristic(self):
		cost = 0
		for x in range(self.size):
			diff = abs(self.stack[x] - self.stack[x+1])
			if(diff > 1):
				cost += 1
		self.forward_cost = cost
		return cost

	def flip(self, location):
		temp, x = 0, 0
		while(x < location):
			temp = self.stack[x]
			self.stack[x] = self.stack[location]
			self.stack[location] = temp
			x += 1
			location -= 1

	def update_costs(self):
		self.back_cost += 1
		self.forward_cost = self.heuristic()
		self.total_cost = self.back_cost + self.forward_cost

	def print_stack(self):
		print_string = "Stack: "
		for i in range(len(self.stack)):
			print_string += str(self.stack[i]) + " "
		print(print_string)

def astar(pancakes):
	print("Running A* on list...")
	print("Initial List: ")
	pancakes.print_stack()

	frontier = pQueue()
	frontier.put(pancakes, pancakes.total_cost)

	visited = {}
	visited[pancakes] = None

	cost = {}
	cost[pancakes] = 0

	G = nx.Graph()
	G.add_node(pancakes)

	counter = 0

	while(not frontier.empty()):
		current = frontier.get()

		if(current.check_order()):
			# print("\nFINAL: ")
			# current.print_stack()
			path = [current]
			while current in visited:
				current = visited[current]
				if(current == None):
					break
				path.append(current)
			path.reverse()
			return path

		counter += 1
		for x in range(current.size):
			temp = copy.deepcopy(current)
			temp.update_costs()
			temp.flip(x+1)
			if(temp in visited):
				continue
			G.add_node(temp)
			G.add_edge(current, temp)

			temp_cost = temp.total_cost
			if temp not in cost or temp_cost < cost[temp]:
				cost[temp] = temp_cost
				frontier.put(temp, temp.total_cost)
				visited[temp] = current

	return visited

def main():
	stack = [3, 2, 5, 1, 6, 4, 7]
	p = Pancakes(stack, 0)
	visited = astar(p)
	print("")
	for i in visited:
		i.print_stack()
	print("")
	print("FINAL: ")
	visited[len(stack)-2].print_stack()


if __name__=='__main__':
	main()