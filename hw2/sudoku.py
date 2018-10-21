import itertools
import sys
import time

characters = 'ABCDEFGHI'
numbers = '123456789'

#***************************************************
#                 Helper Functions
#***************************************************

# Combines the items x and y passed
def combine(x, y):
	return [i + j for i in x for j in y]

# Finds all permutations of a combination passed into it
def permute(combination):
	result = list()
	for x in range(0, len(combination) + 1):
		if(x == 2):
			for subset in itertools.permutations(combination, x):
				result.append(subset)
	return result

# Returns the number of conflicts in a sudoku board
def conflicts(sudoku, var, val):
	count = 0
	for n in sudoku.neighbors[var]:
		if len(sudoku.domains[n]) > 1 and val in sudoku.domains[n]:
			count += 1
	return count

# Function to print the initial state of the board
def print_initial_board(board):
	string = ''
	count = 1
	for x in board:
		if(x == '0'):
			string = string + '  '
		else:
			string = string + x + ' '
		if(count % 9 == 0):
			string += '\n'
		elif(count % 3 == 0):
			string += '|'
		if(count % 27 == 0 and count != 81):
			string += '-------------------\n'
		count += 1
	print(string)

#***************************************************
#                 Sudoku Class
#***************************************************

# Defines the Sudoku class used to contain the board
class Sudoku:

	# Constructor function which sets the board variables
	def __init__(self, board):
		self.variables = []
		self.domains = {}
		self.constraints = []
		self.neighbors = {}
		self.pruned = {}
		self.initialize(board)

	# Initialies the variables of the sudoku object
	#	based on the board passed to it
	def initialize(self, board):
		game = list(board)
		self.variables = combine(characters, numbers)
		for i, v in enumerate(self.variables):
			if(game[i] == '0'):
				self.domains[v] = list(range(1, 10))
				self.pruned[v] = []
			else:
				self.domains[v] = [int(game[i])]
				self.pruned[v] = [int(game[i])]
		self.constrain()
		self.populate()

	# Defines and sets the constraints of the board
	def constrain(self):
		x = ([combine(characters, number) for number in numbers] +
			[combine(character, numbers) for character in characters] +
			[combine(character, number) for character in ('ABC', 'DEF', 'GHI') for number in ('123', '456', '789')])
		for i in x:
			combinations = permute(i)
			for j in combinations:
				if([j[0], j[1]] not in self.constraints):
					self.constraints.append([j[0], j[1]])

	# Populates the object with neighbors
	def populate(self):
		for i in self.variables:
			self.neighbors[i] = []
			for j in self.constraints:
				if i == j[0]:
					self.neighbors[i].append(j[1])

	# Checks if the sudoku game has been solved
	def solved(self):
		for x in self.variables:
			if(len(self.domains[x]) > 1):
				return False
		return True

	# Checks if the board is consistent in its variables
	def consistent(self, assignment, var, value):
		for key, val in assignment.iteritems():
			if val == value and key in self.neighbors[var]:
				return False
		return True

	# Assigns a value to a specific position
	def assign(self, var, value, assignment):
		assignment[var] = value
		self.forward_check(var, value, assignment)

	# Unassigns a value to a specific position
	def unassign(self, var, assignment):
		if var in assignment:
			for (d, v) in self.pruned[var]:
				self.domains[d].append(v)
			self.pruned[var] = []
			del assignment[var]

	# Checks if domains will be altered due to an assignment
	def forward_check(self, var, value, assignment):
		for neighbor in self.neighbors[var]:
			if neighbor not in assignment:
				if value in self.domains[neighbor]:
					self.domains[neighbor].remove(value)
					self.pruned[var].append((neighbor, value))

#***************************************************
#                   AC3 Class
#***************************************************

# Class for the Arc Consistency 3 Algorithm
class ac3:

	# Constructor for the Algorithm object
	def __init__(self, board):
		self.sudoku = Sudoku(board)

	# Solves the sudoku game
	def solve(self):
		if not self.sudoku.solved():
			assignment = {}
			for x in self.sudoku.variables:
				if len(self.sudoku.domains[x]) == 1:
					assignment[x] = self.sudoku.domains[x][0]
			assignment = self.backtrack(assignment)
			for d in self.sudoku.domains:
				self.sudoku.domains[d] = assignment[d] if len(d) > 1 else sudoku.domains[d]
			if not assignment:
				print("Error: No solution to Sudoku board.")

	# Backtrack function to reduce conflicts
	def backtrack(self, assignment):
		if len(assignment) == len(self.sudoku.variables):
			return assignment
		var = self.select_unassigned_variable(assignment)
		for value in self.order_domain_values(var):
			if self.sudoku.consistent(assignment, var, value):
				self.sudoku.assign(var, value, assignment)
				result = self.backtrack(assignment)
				if result:
					return result
				self.sudoku.unassign(var, assignment)
		return False

	def select_unassigned_variable(self, assignment):
		unassigned = [x for x in self.sudoku.variables if x not in assignment]
		return min(unassigned, key=lambda var: len(self.sudoku.domains[var]))

	def order_domain_values(self, var):
		if(len(self.sudoku.domains[var]) == 1):
			return self.sudoku.domains[var]
		return sorted(self.sudoku.domains[var], key=lambda val: conflicts(self.sudoku, var, val))

	# Prints the completed Sudoku board
	def print_solved_board(self):
		string = ''
		count = 1
		for var in self.sudoku.variables:
			string = string + str(self.sudoku.domains[var]) + ' '
			if(count % 9 == 0):
				string += '\n'
			elif(count % 3 == 0):
				string += '|'
			if(count % 27 == 0 and count != 81):
				string += '-------------------\n'
			count += 1
		print(string)

def main():

	# SWITCH BETWEEN SUDOKU BOARDS HERE ---------------------------------------------------------

	# Easy
	# board = '608702100400010002025400000701080405080000070509060301000006750200090008006805203'

	# Hard
	# board = '070042000000008610390000007000004009003000700500100000800000076054800000000610050'

	# Very Hard
	board = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'

	#--------------------------------------------------------------------------------------------

	print("Initial Board:")
	print_initial_board(board)

	game_board = ac3(board)

	start_time = time.time()
	game_board.solve()
	end_time = time.time()

	print("Final Board:")
	game_board.print_solved_board()

	print("Solve Time: " + str(end_time - start_time) + " seconds")


if __name__=='__main__':
	main()