import norvig

########################### FACTOR PARAMETERS ##############################

###### Originial Parameters ######

# FP1_1 = 30
# FP1_2 = 0

# FP2_1 = 1
# FP2_2 = 1

# FP3_1 = 1
# FP3_2 = 1

# FP4_1 = 1
# FP4_2 = 1

# FP5_1 = 3
# FP5_2 = 3

# FP6_1 = 2
# FP6_2 = 10

############ Old Data ###########

# FP1_1 = 2
# FP1_2 = 2

# FP2_1 = 1
# FP2_2 = 2

# FP3_1 = 1
# FP3_2 = 2

# FP4_1 = 1
# FP4_2 = 2

# FP5_1 = 1
# FP5_2 = 0

# FP6_1 = 4
# FP6_2 = 23

############ New Data ###########

FP1_1 = 28
FP1_2 = 0

FP2_1 = 2
FP2_2 = 2

FP3_1 = 2
FP3_2 = 2

FP4_1 = 2
FP4_2 = 2

FP5_1 = 2
FP5_2 = 0

FP6_1 = 3
FP6_2 = 27


############################ UTILITY FUNCTIONS #############################
 
def common(set1, set2):
	return [s for s in set1 if s in set2]

def get_values (grid_vals):

	filld_squares = grid_vals.keys()
	empty_squares = [s for s in norvig.squares if s not in filld_squares]
	values = dict((s, norvig.digits) for s in empty_squares)
	for s in filld_squares:
		num = grid_vals[s]
		for u in norvig.units[s]:
			e = [elem for elem in u if elem in empty_squares]
			for t in e:
				values[t] = values[t].replace(num,'')
	return values


def grid_values(grid):
	grid_vals_full = norvig.grid_values(grid)
	return dict([pair for pair in grid_vals_full.items() if pair[1] in norvig.digits])


########################### FACTOR CLASSIFIERS #############################

def factor1 (grid_vals, p1=FP1_1, p2=FP1_2):
	no_of_givens = len(grid_vals)
	return no_of_givens < p1

def factor2 (grid_vals, p1=FP2_1, p2=FP2_2):
	keys = grid_vals.keys()
	good_units = [unit for unit in norvig.sqr_units if len(common(unit, keys)) <= p1]
	return len(good_units) > p2

def factor3 (grid_vals, p1=FP3_1, p2=FP3_2):
	keys = grid_vals.keys()
	good_units = [unit for unit in norvig.row_units if len(common(unit, keys)) <= p1]
	return len(good_units) > p2

def factor4 (grid_vals, p1=FP4_1, p2=FP4_2):
	keys = grid_vals.keys()
	good_units = [unit for unit in norvig.col_units if len(common(unit, keys)) <= p1]
	return len(good_units) > p2

def factor5 (grid_vals, p1=FP5_1, p2=FP5_2):

	good_digits = [digit for digit in norvig.digits if grid_vals.values().count(digit) < p1]
	return len(good_digits) > p2

def factor6 (grid_vals, p1=FP6_1, p2=FP6_2):

	num = len([val for val in get_values(grid_vals).values() if len(val) <= p1])
	return num <= p2


def main():
	grid = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
	grid = "417369825632158947958724316825437169791586432346912758289643571573291684164875293"
	grid_vals_full = norvig.grid_values(grid)
	grid_vals = grid_values(grid)
	print grid_vals

	norvig.display(grid_vals_full)

	print factor1(grid_vals)
	print factor2(grid_vals)
	print factor3(grid_vals)
	print factor4(grid_vals)
	print factor5(grid_vals)
	print factor6(grid_vals)

if __name__ == "__main__":
	main()
	