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



if __name__ == '__main__':

	analyser = data_analyser()

	analyser.draw_relevance([1,2,3,4,5], [10,20,30,40,50], "data1_name", "data2_name")
