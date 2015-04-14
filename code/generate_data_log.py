import data_process
import classifier
import random
import csv
import math

TIME = 'time'
CSV_FILE = 'output/log_data.csv'
COUNT = 10

def qwatra_categorize(time):
	if time < 500:
		return "CLASS1"
	elif time < 750:
		return "CLASS2"
	elif time < 1000:
		return "CLASS3"
	elif time < 1250:
		return "CLASS4"
	elif time < 1500:
		return "CLASS5"
	elif time < 1750:
		return "CLASS6"
	elif time < 2000:
		return "CLASS7"
	else:
		return "CLASS8"

def toint(b):
	if b:
		return 1
	else:
		return -1

def to_sec(time):
	segs = time.split(':')
	assert len(segs) == 3
	for i in range(3):
		segs[i] = int(segs[i])
	return segs[2] + 60*segs[1] + 60*60*segs[0]

def print_counts(dic):
	print len(dic)
	lens = [len(val) for val in dic.values()]
	lens.sort()
	print "No of categories - "  + str(len(dic))
	print lens
	print "Total - " + str(sum(lens))

def reduce_sudokus():
	sudokus = data_process.load_data_new()
	dic = {}
	for s in sudokus:
		puzzle = classifier.grid_values(s['puzzle'])
		f1 = classifier.factor1(puzzle)
		f2 = classifier.factor2(puzzle)
		f3 = classifier.factor3(puzzle)
		f4 = classifier.factor4(puzzle)
		f5 = classifier.factor5(puzzle)
		f6 = classifier.factor6(puzzle)
		key = (f1, f2, f3, f4, f5, f6)
		#key = (f2, f3, f4, f5, f6)

		if key not in dic.keys():
			dic[key] = []
		s[TIME] = to_sec(s[TIME])
		#s[TIME] = int(s[TIME])
		dic[key].append(s)
	print_counts(dic)

	for key in dic.keys():
		val = dic[key]
		if len(val) < COUNT:
			new_val = []
			for i in range(len(values)):
				s=val[i%len(val)]
				s[TIME]=math.log(s[TIME])
				new_val.append(s)
			dic[key] = new_val
			continue
		no_of_s = min(len(val), random.randint(14, 17))
		no_of_s = COUNT
		new_val = val[0:no_of_s]
		for i in range(no_of_s):
			times = [val[j][TIME] for j in range(i, len(val), no_of_s)]
			avg_time = sum(times)/len(times)
			new_val[i][TIME] = math.log(avg_time)
		dic[key] = new_val
	print_counts(dic)
	return dic

def write_to_csv(dic):
	with open(CSV_FILE, 'wb') as csvfile:
		w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		w.writerow(["f1","f2","f3","f4","f5","f6","time"])
		for key in dic.keys():
			for s in dic[key]:
				# w.writerow([s['puzzle'], s[TIME]])
				w.writerow([toint(key[0]), toint(key[1]), toint(key[2]), toint(key[3]), toint(key[4]), toint(key[5]), s[TIME]])
				
def analyze(dic, index):
	index = index - 1
	trues = sum([dic[k] for k in dic.keys() if k[index]], [])
	falses = sum([dic[k] for k in dic.keys() if not k[index]], [])

	sum1 = sum([s[TIME] for s in trues])
	cnt1 = len(trues)
	sum2 = sum([s[TIME] for s in falses])
	cnt2 = len(falses)

	print 'Total = ' + str(cnt1 + cnt2)
	print 'Trues = ' + str(cnt1)
	print 'Avg time = ' + str(sum1/cnt1)
	print 'Falses = ' + str(cnt2)
	print 'Avg time = ' + str(sum2/cnt2) 

def main():
	dic = reduce_sudokus()
	write_to_csv(dic)
	#analyze(dic, 1)

if __name__ == '__main__':
	main()
