import time
import pandas as pd
import json
import csv
import os
#first_year = "5"
#second_year = "6"
#weight_first_year = "2017"
#weight_second_year = "2018_1"
#k = 0.2

#calculate the sim
def cal_sim(commu1, commu2, weight, k1, k2):
	hit = 0
	res = 0
	if(len(commu1)>10):
		dict = {}
		for r in commu1:
			dict[r] = weight[r]
		sorted(dict.items(),key = lambda x:x[1],reverse = True)
		length = int(len(commu1)*0.3)
		index = 0
		for key,val in dict.items():
			index+=1
			if index>length:
				break
			for n in commu2:
				if n == key:
					hit+=1
					break
		res = float(hit)/length
		res = float(res >= k1)*res
	else:
		for n1 in commu1:
			for n2 in commu2:
				if n1 == n2:
					hit+=1
					break
		res = float(hit)/len(commu1)
		res = float(res >= k2)*res


	return res

def extract_relation(first_year, second_year, weight_first_year, weight_second_year, k1, k2):
	csv_reader1 = csv.reader(open("data/smooth_community{}.csv".format(first_year)))
	csv_reader2 = csv.reader(open("data/smooth_community{}.csv".format(second_year)))
	csv_reader3 = csv.reader(open("data/smooth_repo_weight{}.csv".format(first_year)))
	csv_reader4 = csv.reader(open("data/smooth_repo_weight{}.csv".format(second_year)))
	csv_reader5 = csv.reader(open("data/weight{}.csv".format(weight_first_year)))
	csv_reader6 = csv.reader(open("data/weight{}.csv".format(weight_second_year)))
	communities1 = []
	communities2 = []
	communities1_name = []
	communities2_name = []
	weight = {}
	for row in csv_reader1:
		communities1.append(row)
	for row in csv_reader2:
		communities2.append(row)
	for row in csv_reader3:
		communities1_name.append(row[1])
	for row in csv_reader4:
		communities2_name.append(row[1])

	for row in csv_reader5:
		weight[row[0]] = int(row[1])
	for row in csv_reader6:
		weight[row[1]] = int(row[1])

	len1 = len(communities1)
	len2 = len(communities2)
	#print("len1",len1)
	#print("len2",len2)
	c1_c2 = {}
	c2_c1 = {}

	for i in range(len(communities1)):
		for j in range(len(communities2)):
			sim = cal_sim(communities1[i], communities2[j], weight, k1, k2)
			if sim > 0:
				if i in c1_c2:
					c1_c2[i].append(j)
				else:
					c1_c2[i] = []
					c1_c2[i].append(j)

				if j in c2_c1:
					c2_c1[j].append(i)
				else:
					c2_c1[j] = []
					c2_c1[j].append(i)
	print(len(c1_c2))
	print(len(c2_c1))
	split = []
	dissolve = []
	survive = []
	for i in range(len1):
		#print("i=",i)
		if i in c1_c2:
			size = len(c1_c2[i])
		else:
			size = 0

		info = []
		info.append(i)
		if size == 0:
			dissolve.append(info)
		elif size == 1:
			for j in c1_c2[i]:
				info.append(j)
			survive.append(info)
		else:
			for j in c1_c2[i]:
				info.append(j)
			split.append(info)

	form = []
	merge = []

	for i in range(len2):
		if i in c2_c1:
			size = len(c2_c1[i])
		else:
			size = 0
		info = []
		info.append(i)
		if size == 0:
			form.append(info)
		elif size >= 2:
			for j in c2_c1[i]:
				info.append(j)
			merge.append(info)
	with open('result/split_{}_{}.csv'.format(first_year,second_year), 'w', newline = '') as csvfile:
		writer = csv.writer(csvfile)
		for row in split:
			writer.writerow(row)
	with open('result/dissolve_{}_{}.csv'.format(first_year,second_year), 'w', newline = '') as csvfile:
		writer = csv.writer(csvfile)
		for row in dissolve:
			writer.writerow(row)
	with open('result/survive_{}_{}.csv'.format(first_year,second_year), 'w', newline = '') as csvfile:
		writer = csv.writer(csvfile)
		for row in survive:
			writer.writerow(row)
	with open('result/form_{}.csv'.format(second_year), 'w', newline = '') as csvfile:
		writer = csv.writer(csvfile)
		for row in form:
			writer.writerow(row)
	with open('result/merge_{}.csv'.format(second_year), 'w', newline = '') as csvfile:
		writer = csv.writer(csvfile)
		for row in merge:
			writer.writerow(row)

	return split, dissolve, survive, form, merge
