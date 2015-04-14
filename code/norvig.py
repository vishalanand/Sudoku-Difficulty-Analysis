## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
from random import randint
import random
import time
from generate import generate

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
sqr_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print 'All tests pass.'

################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values

################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print

################ Search ################

def solve(grid, soln=False): return search(parse_grid(grid), soln)

def search(values, soln):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        if soln != False and values == soln:
            return False
        else:
            return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d), soln)
                for d in values[s])

################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return file(filename).read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ System test ################

import time, random

def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print '(%.2f seconds)\n' % t
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
    return random_puzzle(N) ## Give up and make a new puzzle


################ creating partially filled sudokus ################

def remove_element(grid, new_grid):
    indices = [i for i in range(81) if new_grid[i] in digits]
    if len(indices) == 0:
        return -1
    pos = random.choice(indices)
    return pos


# def remove_element(grid):
#     gridtemp = grid.replace('.','')
#     random.randint(1,len(grid))

def remove_n_elements(grid, new_grid, soln, n):
    if n == 0:
        return grid
    while True:
        pos = remove_element(grid, new_grid)
        if pos == -1:
            return False
        temp_grid = grid[:pos] + '.' + grid[pos+1:]
        print temp_grid
        temp_new_grid = new_grid[:pos] + '.' + new_grid[pos+1:]
        if not exist_more_solns(temp_grid, soln):
            result_grid = remove_n_elements(temp_grid, temp_new_grid, soln, n-1)
            if result_grid == False:
                new_grid = new_grid[:pos] + '*' + new_grid[pos+1:]
            else:
                return result_grid
        else:        
            print 'failed'
            print temp_grid
            new_grid = new_grid[:pos] + '*' + new_grid[pos+1:]
    # pos = remove_element(grid, new_grid)
    # if pos == -1:
    #     return False
    # while True:
    #     temp_grid = grid[:pos] + '.' + grid[pos+1:]
    #     temp_new_grid = new_grid[:pos] + '.' + new_grid[pos+1:]
    #     if !exist_more_solns(temp_grid, soln):
    #         result_grid = remove_element(temp_grid, temp_new_grid, soln, n-1)
    #         if result_grid != False:
    #             return result_grid
    #         else:
    #             new_grid = new_grid[:pos] + '*' + new_grid[pos+1:]

# def remove_n_elements(grid,soln,n):
#     i=0
#     while i<n:
#         new_grid = grid[:]
#         while True:
#             grid, pos, new_grid = remove_element(grid, new_grid)
#             if exist_more_solns(grid,soln):
#                 grid = undo(grid, soln, pos)
#                 new_grid = new_grid[:pos] + '*' + new_grid[pos+1:]
#             else:
#                 break
#         print i
#         i+=1
#     return grid

def undo(grid, soln, pos):
    grid = grid[:pos] + soln[pos] + grid[pos+1:]
    return grid

def create_problem(soln, num_givens):
    random.seed(time.time())
    # print grid
    grid = soln
    num_removals = 81 - num_givens
    grid = remove_n_elements(grid,grid,soln,num_removals)
    assert grid != False
    #print count_params(grid)
    #display(grid_values(grid))
    return grid

def exist_more_solns(grid, soln):
    soln_vals = grid_values(soln)
    solved_mul = solve(grid, soln_vals)
    a=''
    for i in solved_mul.keys():
        a+=str(solved_mul[i])
    print a
    return solved_mul

    # if solved_mul == False:
    #     print 'Only one solution'
    # else:
    #     print 'more solns'
    #     # display(solved_mul)

################ exs ################

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

soln_grid2 = '417369825632158947958724316825437169791586432346912758289643571573291684164875293'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

mul = '9.6.7.4.3...4..2...7..23.1.5.....1...4.2.8.6...3.....5.3.7...5...7..5...4.5.1.7.8'
solved_mul = '926571483351486279874923516582367194149258367763149825238794651617835942495612738'


if __name__ == '__main__':
    # create_problem(soln_grid2,43)
    exist_more_solns('.1...9825632158.4..5.72.3...2..3..6..9...6432.4691...8..96.3..1.7329.68.164.75.9.',soln_grid2)
 #   test()
#    solve_all(from_file("easy50.txt", '========'), "easy", None)
#    solve_all(from_file("top95.txt"), "hard", None)
#    solve_all(from_file("hardest.txt"), "hardest", None)
#    solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
    # for i in range(40, 24, -1):
    #     f = open('sudokusv2/file'+str(i)+'.txt','w')
    #     start = time.time()
    #     for j in range(500):
    #         st = generate()
    #         f.write(create_problem(st, i) + ' ' + st)
    #         f.write('\n')
    #     f.close()
    #     end = time.time()
    #     print '#Givens = ',i ,' Time: ', str(end-start)
        # unsolved_mul = grid_values(mul)
    # display(unsolved_mul)

    # solved_mul_vals = grid_values(solved_mul)
    # display(solved_mul_vals)

    # solved_mul = solve(mul, solved_mul_vals)
    # if solved_mul == False:
    #     print 'Only one solution'
    # else:
    #     display(solved_mul)

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
