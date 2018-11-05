import os, sys
import random
import copy

INITIAL_POPULATION = 50
NUM_GENERATIONS = 40

#***************************************************
#				 Helper Functions
#***************************************************

def initialize_problem(weights, values):
	if(len(weights) != len(values)):
		print("Incompatible Lists (weights & values).")
		sys.exit()
	weight, value = "", ""
	for i in range(len(weights)):
		weight += "%0.2d " % weights[i]
		value += " %0.1d " % values[i]
	print("Items List:")
	print("  Weights: " + weight)
	print("  Values:  " + value)
	print("===== Starting Genetic Algorithm =====\n")

def finalize_problem(chromosome, fitness, weights):
	print("\n===== Quitting Genetic Algorithm ====\n")
	items = ""
	for i in range(len(chromosome)):
		if(chromosome[i] == 1):
			items += "%0.2d " % weights[i]
	print("Number of Generations: " + str(NUM_GENERATIONS))
	print("Optimal Chromosome: " + str(chromosome))
	print("Optimal Items: "+ items)
	print("Total Value of Items: " + str(fitness) + "\n")

def starting_population(amount, num_items):
	return [rand_individual(num_items) for i in range(0, amount)]

def rand_individual(num_items):
	return [random.randint(0,1) for i in range(0, num_items)]

#***************************************************
#				  Item Class
#***************************************************

class item:
	def __init__(self, weight, value):
		self.weight = weight
		self.value = value

#***************************************************
#				 Knapsack Class
#***************************************************

class knapsack():
	def __init__(self, weights, values, max_capacity):
		self.max_capacity = max_capacity
		self.knapsack = []

		#CLEAN UP LOOP... I dislike it
		for i in range(len(weights)):
			self.knapsack.append(item(weights[i], values[i]))

	def generate(self):
		best_chromosome = []
		best_fitness = 0
		generation = 1
		population = starting_population(INITIAL_POPULATION, len(self.knapsack))
		for i in range(0, NUM_GENERATIONS):
			population = sorted(population, key=lambda x: self.fitness(x), reverse=True)
			if(self.fitness(population[0]) > best_fitness):
				best_fitness = self.fitness(population[0])
				best_chromosome = copy.deepcopy(population[0])
			print("Gen " + str(i+1) + ": "+ str(population[0]))
			population = self.evolve_population(population)
			generation += 1
		return best_chromosome, best_fitness

	def fitness(self, chromosome):
		value, weight, index = 0, 0, 0
		for i in chromosome:
			if(i == 1):
				value += self.knapsack[index].value
				weight += self.knapsack[index].weight
			index += 1
		if weight > self.max_capacity:
			return 0
		return value

	def mutate(self, chromosome):
		r = random.randint(0, len(chromosome) - 1)
		chromosome[r] = (0 if chromosome[r] == 1 else 0)

	def evolve_population(self, population):
		cull_prob = 0.5
		mutation_chance = 0.15
		lottery = 0.05

		parent_length = int(cull_prob * len(population))
		self.parents = population[:parent_length]
		nonparents = population[parent_length:]

		for np in nonparents:
			if lottery > random.random():
				self.parents.append(np)

		for p in self.parents:
			if mutation_chance > random.random():
				self.mutate(p)

		children = []
		desired_length = len(population) - len(self.parents)
		while len(children) < desired_length:
			male = population[random.randint(0,len(self.parents)-1)]
			female = population[random.randint(0,len(self.parents)-1)]
			half = len(male)/2
			child = male[:half] + female[half:]
			if mutation_chance > random.random():
				self.mutate(child)
			children.append(child)

		self.parents.extend(children)
		return self.parents
	
#***************************************************
#				 Main Function
#***************************************************

def main():

	# CHANGE INITIAL VALUES HERE ----------------------------------------------------------------

	max_capacity = 120
	weights = [20, 30, 60, 90, 50, 70, 30]
	values = [6, 5, 8, 7, 6, 9, 4]

	#--------------------------------------------------------------------------------------------

	initialize_problem(weights, values)
	sack = knapsack(weights, values, max_capacity)
	chromosome, fitness = sack.generate()
	finalize_problem(chromosome, fitness, weights)


if __name__ == '__main__':
	main()