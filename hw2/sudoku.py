import itertools
import sys
import time

# Define constants
character_domains = 'ABCDEFGHI'
char_combo = ('ABC', 'DEF', 'GHI')
number_domains = '123456789'
num_combo = ('123', '456', '789')

#***************************************************
#                 Helper Functions
#***************************************************

# Combines the items x and y passed
def combine(x, y):
	return [i + j for i in x for j in y]

# Finds all permutations of a combination passed into it
def permute(combination):
	result = []
	for x in range(0, len(combination) + 1):
		if(x == 2):
			for subset in itertools.permutations(combination, x):
				result.append(subset)
	return result

# Returns the constraint for a Sudoku board
def get_contraint():
	return ([combine(character_domains, i) for i in number_domains] +
			[combine(i, number_domains) for i in character_domains] +
			[combine(i, j) for i in char_combo for j in num_combo])

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
		self.eliminated = {}
		self.initialize(board)

	# Initialies the variables of the sudoku object
	#	based on the board passed to it
	def initialize(self, board):
		game = list(board)
		self.variables = combine(character_domains, number_domains)
		for x, v in enumerate(self.variables):
			if(game[x] == '0'):
				self.domains[v] = list(range(1, 10))
				self.eliminated[v] = []
			else:
				self.domains[v] = [int(game[x])]
				self.eliminated[v] = [int(game[x])]
		self.constrain()
		self.populate()

	# Defines and sets the constraints of the board
	def constrain(self):
		constraints = get_contraint()
		for i in constraints:
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
		self.check_forward(var, value, assignment)

	# Unassigns a value to a specific position
	def unassign(self, var, assignment):
		if var in assignment:
			for (d, v) in self.eliminated[var]:
				self.domains[d].append(v)
			self.eliminated[var] = []
			del assignment[var]

	# Checks if domains will be altered due to an assignment
	def check_forward(self, var, value, assignment):
		for neighbor in self.neighbors[var]:
			if neighbor not in assignment:
				if value in self.domains[neighbor]:
					self.domains[neighbor].remove(value)
					self.eliminated[var].append((neighbor, value))

#***************************************************
#                   AC3 Class
#***************************************************

# Class for the Arc Consistency 3 (AC3) Algorithm
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
				print("Error: No Solution Exists.")

	# Backtrack function to reduce conflicts
	def backtrack(self, assignment):
		if len(assignment) == len(self.sudoku.variables):
			return assignment
		var = self.select_variable(assignment)
		for value in self.order_domains(var):
			if self.sudoku.consistent(assignment, var, value):
				self.sudoku.assign(var, value, assignment)
				result = self.backtrack(assignment)
				if result:
					return result
				self.sudoku.unassign(var, assignment)
		return False

	# Selects variables for backtracking
	def select_variable(self, assignment):
		unassigned = [x for x in self.sudoku.variables if x not in assignment]
		return min(unassigned, key=lambda var: len(self.sudoku.domains[var]))

	# Orders the domains in a Sudoku board
	def order_domains(self, var):
		if(len(self.sudoku.domains[var]) == 1):
			return self.sudoku.domains[var]
		return sorted(self.sudoku.domains[var], key=lambda val: self.conflicts(var, val))

	# Returns the number of conflicts in a sudoku board
	def conflicts(self, var, val):
		count = 0
		for x in self.sudoku.neighbors[var]:
			if len(self.sudoku.domains[x]) > 1 and val in self.sudoku.domains[x]:
				count += 1
		return count

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

#***************************************************
#                 Main Function
#***************************************************

def main():

	# SWITCH BETWEEN SUDOKU BOARDS HERE ---------------------------------------------------------

	# Easy
	#board = '608702100400010002025400000701080405080000070509060301000006750200090008006805203'

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