#!/usr/bin/env python
#coding: utf-8

class normalizer(object):

	def linear_normalize(self, data_list):

		max_num = data_list[0]
		min_num = data_list[0]

		for num in data_list:
			if num > max_num:
				max_num = num
			elif num < min_num:
				min_num = num

		gap = max_num - min_num

		if gap == 0:
			gap = max_num

		result = []

		for i in range(len(data_list)):
			result.append(float(data_list[i] - min_num) / float(gap))

		return result


if __name__ == '__main__':
	norm = normalizer()
	a = [0,1,2,3,4,5,6,7,8,9,10]
	print a
	print norm.linear_normalize(a)
