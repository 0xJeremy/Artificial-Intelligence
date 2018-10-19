import itertools
import sys
import time

characters = 'ABCDEFGHI'
numbers = '123456789'

#***************************************************
#                 Helper Functions
#***************************************************
def constraint(xi, xj):
	return xi != xj

def combine(x, y):
	return [i + j for i in x for j in y]

def permute(combination):
	result = list()
	for x in range(0, len(combination) + 1):
		if(x == 2):
			for subset in itertools.permutations(combination, x):
				result.append(subset)
	return result

def conflicts(sudoku, var, val):
	count = 0
	for n in sudoku.neighbors[var]:
		if len(sudoku.domains[n]) > 1 and val in sudoku.domains[n]:
			count += 1
	return count

def print_initial_board(board):
	string = ''
	count = 1
	for x in board:
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
class Sudoku:

	def __init__(self, board):
		self.variables = []
		self.domains = {}
		self.constraints = []
		self.neighbors = {}
		self.pruned = {}
		self.initialize(board)

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

	def constrain(self):
		x = ([combine(characters, number) for number in numbers] +
			[combine(character, numbers) for character in characters] +
			[combine(character, number) for character in ('ABC', 'DEF', 'GHI') for number in ('123', '456', '789')])
		for i in x:
			combinations = permute(i)
			for j in combinations:
				if([j[0], j[1]] not in self.constraints):
					self.constraints.append([j[0], j[1]])

	def populate(self):
		for i in self.variables:
			self.neighbors[i] = []
			for j in self.constraints:
				if i == j[0]:
					self.neighbors[i].append(j[1])

	def solved(self):
		for x in self.variables:
			if(len(self.domains[x]) > 1):
				return False
		return True

	def complete(self, assignment):
		for x in self.variables:
			if len(self.domains[x]) > 1 and x not in assignment:
				return False
		return True

	def consistent(self, assignment, var, value):
		consistent = True
		for key, val in assignment.iteritems():
			if val == value and key in self.neighbors[var]:
				consistent = False

		return consistent

	def assign(self, var, value, assignment):
		assignment[var] = value
		self.forward_check(var, value, assignment)

	def unassign(self, var, assignment):
		if var in assignment:
			for (D, v) in self.pruned[var]:
				self.domains[D].append(v)
			self.pruned[var] = []
			del assignment[var]

	def forward_check(self, var, value, assignment):
		for neighbor in self.neighbors[var]:
			if neighbor not in assignment:
				if value in self.domains[neighbor]:
					self.domains[neighbor].remove(value)
					self.pruned[var].append((neighbor, value))

#***************************************************
#                   AC3 Class
#***************************************************
class ac3:
	def __init__(self, board):
		self.sudoku = Sudoku(board)

	def ac3_solve(self):
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

	def solve(self):
		queue = list(self.sudoku.constraints)
		while(len(queue) != 0):
			xi, xj = queue.pop(0)
			if revise(xi, xj):
				if(len(self.sudoku.domains[xi]) == 0):
					return False
				for xk in self.sudoku.neighbors[xi]:
					if xk != xi:
						queue.append([xk, xi])
		return True

	def revise(self, xi, xj):
		temp = False
		for x in self.sudoku.domains[xi]:
			if not any([self.sudoku.constraint(x, y) for y in self.sudoku.domains[xj]]):
				self.sudoku.domains[xi].remove(x)
				temp = True
		return temp

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

	def print_board(self):
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

	# board = '608702100400010002025400000701080405080000070509060301000006750200090008006805203'
	# board = '070042000000008610390000007000004009003000700500100000800000076054800000000610050'
	board = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'

	#--------------------------------------------------------------------------------------------

	print("Initial Board:")
	print_initial_board(board)

	solved_board = ac3(board)

	start_time = time.time()
	solved_board.ac3_solve()
	end_time = time.time()

	print("Final Board:")
	solved_board.print_board()

	print("Solve Time: " + str(end_time - start_time) + " seconds")


if __name__=='__main__':
	main()