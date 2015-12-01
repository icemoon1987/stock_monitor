#!/usr/bin/env python
#coding: utf-8

import matplotlib.pyplot as plt
from normalizer import normalizer

class data_analyser(object):

	def draw_relevance(self, data1, data2, data1_name, data2_name):

		norm = normalizer()

		data1_norm = norm.linear_normalize(data1)
		data2_norm = norm.linear_normalize(data2)

		plt.figure(1)
		plt.subplot(211)
		plt.plot(data1, 'b-', data2, 'r-')
		plt.legend([data1_name, data2_name], loc="upper left")

		plt.subplot(212)
		plt.plot(data1_norm, 'b-', data2_norm, 'r-')
		plt.legend([data1_name, data2_name], loc="upper left")
		plt.grid(True)
		plt.show()

		return


	def calcu_mean_line(self, data, k):

		result = []

		for i in range(len(data)):
			if i < k-1:
				result.append(0)
			else:
				sum = 0
				for num in data[i-k+1 : i+1]:
					sum += num

				result.append(float(sum / (k * 1.0)))

		return result


	def find_max(self, data):
		max = data[0]

		for num in data:
			if num > max:
				max = num

		return max

	def find_min(self, data):
		min = data[0]

		for num in data:
			if num < min:
				min = num

		return min

	def calcu_max_line(self, data, k):
		result = []

		for i in range(len(data)):
			if i < k:
				result.append(0)
			else:
				result.append(self.find_max(data[i-k : i]))

		return result

	def calcu_min_line(self, data, k):
		result = []

		for i in range(len(data)):
			if i < k:
				result.append(0)
			else:
				result.append(self.find_min(data[i-k : i]))

		return result

if __name__ == '__main__':

	analyser = data_analyser()

	#analyser.draw_relevance([1,2,3,4,5], [10,20,30,40,50], "data1_name", "data2_name")

	test_data = range(100)
	print test_data
	mean_line = analyser.calcu_mean_line(test_data, 10)
	print mean_line
	max_line = analyser.calcu_max_line(test_data, 10)
	print max_line
	min_line = analyser.calcu_min_line(test_data, 10)
	print min_line

	"""
	plt.figure(1)
	plt.plot(test_data, 'b-', mean_line, 'r-', max_line, 'y-', min_line, 'k-')
	plt.legend(["test_data", "mean_line", "max_line", "min_line"], loc="upper left")
	plt.grid(True)
	plt.show()
	"""

