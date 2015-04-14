import os
import json
import classifier
import textwrap
import generate_data

def  load_data(filename):
	sudokus = []
	with open(filename) as json_file:
		sudokus = json.load(json_file)
	return sudokus

def give_counts(sudokus):
	dic = {}
	for s in sudokus:
		puzzle = classifier.grid_values(s['puzzle'])
		f_vals = (classifier.factor1(puzzle), classifier.factor2(puzzle),\
	#	f_vals = (classifier.factor2(puzzle),\
		classifier.factor3(puzzle), classifier.factor4(puzzle), classifier.factor5(puzzle),\
		classifier.factor6(puzzle))
		if f_vals not in dic.keys():
			dic[f_vals] = []
		dic[f_vals].append(puzzle)
	print len(sudokus)
	for key in dic.keys():
		print str(key) + " " + str(len(dic[key]))
	lens = [len(val) for val in dic.values()]
	lens.sort()
	print lens
	print "Total categories - " + str(len(lens))

def find_opt_param(sudokus, func, l1, u1, l2, u2):
	lst = []
	for p1 in range(l1, u1+1):
		for p2 in range(l2, u2+1):
			less = len([s for s in sudokus if func(classifier.grid_values(s['puzzle']), p1, p2)])
			more = len(sudokus) - less
			triple = (abs(more-less), p1, p2)
			print triple
			lst.append(triple)
	print min(lst)


def load_data_old():
	filename = "data/old_data/finaldata.json"
	return load_data(filename)


def format_new_data (grid):
	l1 = textwrap.wrap(grid, 27)
	ngrid = ""
	for l in l1:
		l2 = textwrap.wrap(l, 9)
		for i in range(3):
			l2[i] = textwrap.wrap(l2[i], 3)
		for i in range(3):
			for j in range(3):
				ngrid += l2[j][i]
	return ngrid

def load_data_new():

	f1 = "data/new_data/easy_data.json"
	f2 = "data/new_data/hard_data.json"
	f3 = "data/new_data/vhard_data.json"
	f4 = "data/new_data/easy_data1.json"
	f5 = "data/new_data/hard_data1.json"

	s1 = load_data(f1)
	s2 = load_data(f2)
	s3 = load_data(f3)
	s4 = load_data(f4)
	s5 = load_data(f5)

	sudokus = s1 + s2 + s3 + s4 + s5
	for dic in sudokus:
		dic['puzzle'] = format_new_data(dic['puzzle'])

	strings = [dic['puzzle'] for dic in sudokus]
	cnts = [strings.count(elem) for elem in set(strings)]
	cnts.sort()
	cnts.reverse()
	print cnts
	return sudokus

def analyze(sudokus, func, p1, p2):
	s1 = [s for s in sudokus if func(classifier.grid_values(s['puzzle']), p1, p2)]
	s2 = [s for s in sudokus if s not in s1]

	tt = generate_data.to_sec
	sum1 = sum(tt(s['time']) for s in s1)
	cnt1 = len(s1)
	sum2 = sum(tt(s['time']) for s in s2)
	cnt2 = len(s2)

	print 'Total = ' + str(cnt1 + cnt2)
	print 'Trues = ' + str(cnt1)
	print 'Avg time = ' + str(sum1/cnt1)
	print 'Falses = ' + str(cnt2)
	print 'Avg time = ' + str(sum2/cnt2)


def main():

	sudokus = load_data_new()

#	find_opt_param(sudokus, classifier.factor6, 8, 8, 50, 81)
	give_counts(sudokus)
#	analyze(sudokus, classifier.factor5, classifier.FP5_1, classifier.FP5_2)


if __name__ == "__main__":
	main()