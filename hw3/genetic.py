import os, sys
import random
import copy

#***************************************************
#				 Constant Variables
#***************************************************

INITIAL_POPULATION = 50
NUM_GENERATIONS = 20
CULL_PROBABILITY = 0.5
MUTATION = 0.15
LOTTERY = 0.05

#***************************************************
#				 Helper Functions
#***************************************************

# Prints information about the initial state
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

# Prints information about the solution
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

# Generates a random starting population
def starting_population(amount, num_items):
	return [rand_individual(num_items) for i in range(0, amount)]

# Generates a random individual
def rand_individual(num_items):
	return [random.randint(0,1) for i in range(0, num_items)]

#***************************************************
#				  Item Class
#***************************************************

# Used to store information about each item
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
		for i in range(len(weights)):
			self.knapsack.append(item(weights[i], values[i]))

	# Solves the knapsack problem with a genetic algorithm
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

	# Fitness function defining the fitness of each chromosome
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

	# Mutates a given chromosome
	def mutate(self, chromosome):
		r = random.randint(0, len(chromosome) - 1)
		chromosome[r] = (0 if chromosome[r] == 1 else 0)

	# Evolves the population by culling part of the population
	#	and creating children
	def evolve_population(self, population):
		parent_length = int(CULL_PROBABILITY * len(population))
		parents = population[:parent_length]
		nonparents = population[parent_length:]
		for i in nonparents:
			if LOTTERY > random.random():
				parents.append(i)
		for i in parents:
			if MUTATION > random.random():
				self.mutate(i)
		children = []
		desired_length = len(population) - len(parents)
		while len(children) < desired_length:
			child1 = population[random.randint(0, len(parents)-1)]
			child2 = population[random.randint(0, len(parents)-1)]
			child = child1[:int(len(child1)/2)] + child2[int(len(child1)/2):]
			if MUTATION > random.random():
				self.mutate(child)
			children.append(child)
		parents.extend(children)
		return parents
	
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