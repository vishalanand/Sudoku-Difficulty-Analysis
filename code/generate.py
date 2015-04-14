import numpy as np
from random import randint
import time
import random
############# Utilities ####################

def permutation(n):
	"Gives a random permutation form 0 to n-1"
	if n == 1:
		return [0]
	rint = randint(0, n-1)
	small_perm = permutation(n-1)
	return small_perm[0:rint] + [n-1] + small_perm[rint:n-1]

def permute_rows(arr):
	n = arr.shape[0]
	perm = permutation(n)
	new_arr = np.zeros(arr.shape, dtype=int)
	for i in range(n):
		new_arr[i:i+1, :] = arr[perm[i]:perm[i]+1, :]
	return new_arr

def permute_cols(arr):
	n = arr.shape[1]
	perm = permutation(n)
	new_arr = np.zeros(arr.shape, dtype=int)
	for i in range(n):
		new_arr[:, i:i+1] = arr[:, perm[i]:perm[i]+1]
	return new_arr

def arr_to_str(arr):
	st = ''
	for i in range(9):
		for j in range(9):
			st = st + str(arr[i][j])
	return st

############ 3X3 Latin Square ###############

def latin_square():
	"Gives a 3X3 latin square"
	perm = permutation(3)
	arr = -1*np.ones((3, 3), dtype=np.int)
	for i in range(3):
		arr[i][perm[i]] = 2
	d1 = randint(0, 1)
	d2 = 1-d1
	x = x1 = x2 = x3 = x4 = y = y1 = y2 = y3 = y4 = 0
	y = min([i for i in range(3) if arr[0][i] == -1])
	arr[x][y] = d1
	y1 = y
	x1 = min([i for i in range(3) if arr[i][y1] == -1])
	x2 = 0
	y2 = min([i for i in range(3) if arr[x2][i] == -1])
	arr[x1][y1] = arr[x2][y2] = d2
	x3 = x1
	y3 = min([i for i in range(3) if arr[x3][i] == -1])
	y4 = y2
	x4 = min([i for i in range(3) if arr[i][y4] == -1])
	arr[x3][y3] = arr[x4][y4] = d1
	for i in [j for j in range(3) if arr[j][y3] == -1]:
		arr[i][y3] = d2
	for i in [j for j in range(3) if arr[x4][j] == -1]:
		arr[x4][i] = d2
	return arr

############ Generation Tools ###################

def invalid_sudoku():
	arr = -1*np.ones((9, 9), dtype=int)
	template = latin_square()
	for i in range(3):
		for j in range(3):
			arr[3*i:3*i+3, 3*j:3*j+3] = 3*template[i][j] + latin_square() + 1
	return arr

def valid_sudoku(arr):
	new_arr = np.zeros(arr.shape, dtype=int)
	new_arr[0,:] = arr[0,:]
	new_arr[3,:] = arr[1,:]
	new_arr[6,:] = arr[2,:]
	new_arr[1,:] = arr[3,:]
	new_arr[4,:] = arr[4,:]
	new_arr[7,:] = arr[5,:]
	new_arr[2,:] = arr[6,:]
	new_arr[5,:] = arr[7,:]
	new_arr[8,:] = arr[8,:]
	return new_arr

def mapping(arr):
	perm = permutation(9)
	for i in range(9):
		for j in range(9):
			arr[i][j] = perm[arr[i][j]-1]+1


################# Generate Function ########################

def generate():
	random.seed(time.time())
	arr = invalid_sudoku()
	arr = valid_sudoku(arr)
	arr[0:3, :] = permute_rows(arr[0:3, :])
	arr[3:6, :] = permute_rows(arr[3:6, :])
	arr[6:9, :] = permute_rows(arr[6:9, :])
	for i in range(12):
		pos = randint(0,2)
		if randint(0,1) == 1:
			arr[3*pos:3*pos+3, :] = permute_rows(arr[3*pos:3*pos+3, :])
		else:
			arr[:, 3*pos:3*pos+3] = permute_cols(arr[:, 3*pos:3*pos+3])
	if randint(0, 1) == 1:
		arr = arr.T
	mapping(arr)
	return arr_to_str(arr)


###################### Main ############################

def main():
	print generate()

if __name__ == '__main__':
	main()

