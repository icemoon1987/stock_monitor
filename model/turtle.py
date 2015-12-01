#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import urllib
import myjson
from datetime import *
import time 
from define import *

class turtle(object):
	"""
	turtle model
	"""

	def get_mean(self, data, end_index, k):
		if end_index < k-1:
			return 0
		else:
			sum = 0
			for num in data[end_index-k+1 : end_index+1]:
				sum += num

		return float(sum / (k * 1.0))


	def get_max(self, data, end_index, k):
		if end_index < k:
			return 0
		else:
			tmp = data[end_index-k : end_index]
			max = tmp[0]

			for num in tmp:
				if num > max:
					max = num
		return max

	def get_min(self, data, end_index, k):
		if end_index < k:
			return 0
		else:
			tmp = data[end_index-k : end_index]
			min = tmp[0]

			for num in tmp:
				if num < min:
					min = num
		return min

	def get_trading_plan(self, dataset, date_str):
		"""
		get trading plan of 28 lundong model, return a empty map when no decision can be made

		choise:  
			-3:	not enough data, do not trade
			-2:	date_str error
			-1:	unknown problem, do not trade
			0:	sell all
			1:	sell half
			2:	close_price unsatisfy, do not trade
			3:	mean line unsatisfy, do not trade
			4:	buy
		"""

		result = {}
		result["choise"] = -1

		# Get stock data by date_str. If not exist, return.
		data = dataset.get_data(date_str)
		if data == None:
			result["choise"] = -2
			return result

		data_index = dataset.get_data_index(date_str)
		data_len = len(dataset.data)

		close_prices = [ item.close_price for item in dataset.data ]

		result["close_price"] = close_prices[data_index]
		result["10_mean"] = self.get_mean(close_prices, data_index, 10)
		result["100_mean"] = self.get_mean(close_prices, data_index, 100)
		result["50_max"] = self.get_max(close_prices, data_index, 50)
		result["50_min"] = self.get_min(close_prices, data_index, 50)
		result["25_min"] = self.get_min(close_prices, data_index, 25)

		if result["10_mean"] == 0 or result["100_mean"] == 0 or result["50_max"] == 0 or result["50_min"] == 0 or result["25_min"] == 0:
			result["choise"] = -3
			return result

		if result["close_price"] < result["50_min"]:
			result["choise"] = 0
			return result

		if result["close_price"] < result["25_min"]:
			result["choise"] = 1
			return result

		if result["close_price"] > result["50_max"]:
			if result["10_mean"] < result["100_mean"]:
				result["choise"] = 3
				return result
			else:
				result["choise"] = 4
				return result
		else:
			result["choise"] = 2
			return result

		return result


if __name__ == '__main__':
	pass

