#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")

import matplotlib.pyplot as plt
from model.lundong import lundong
from define import *
from tools.data_analyser import data_analyser
from account_simulator import account_simulator
import math
from datetime import datetime

def get_data(dataset, date_str):
	"""
	get stock data by date_str, return a empty list if not exist
	"""
	for item in dataset:
		if item[DATE_POS] == date_str:
			return item
	return []

def load_data(file_path):
	"""
	load stock data from a file
	"""
	result = []
	print "loading: " + file_path

	f = open(file_path)

	for line in f:
		line = line.decode("utf-8").strip()
		ary = line.split(",")

		if len(ary) != 6:
			continue

		tmp = []
		tmp.append(ary[0])
		tmp.append(float(ary[1]))
		tmp.append(float(ary[2]))
		tmp.append(float(ary[3]))
		tmp.append(float(ary[4]))
		tmp.append(float(ary[5]))

		result.append(tmp)

	return result


def time_align(data1, data2):
	"""
	preprocess data, align two dataset based on date_str
	"""

	i = 0
	while i < len(data1):
		date_str1 = data1[i][DATE_POS]
		flag = False

		for item2 in data2:
			date_str2 = item2[DATE_POS]
			if date_str1 == date_str2:
				flag = True
				break

		# Delete redundant data in dataset1
		if not flag:
			del data1[i]
		else:
			i = i + 1

	i = 0
	while i < len(data2):
		date_str2 = data2[i][DATE_POS]
		flag = False

		for item1 in data1:
			date_str1 = item1[DATE_POS]
			if date_str2 == date_str1:
				flag = True
				break

		# Delete redundant data in dataset2
		if not flag:
			del data2[i]
		else:
			i = i + 1

	return


def time_truncate(data1, data2, start_date_str, end_date_str):

	start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
	end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

	i = 0
	while i < len(data1):
		date1 = datetime.strptime(data1[i][DATE_POS], "%Y-%m-%d")

		# Delete redundant data in dataset1
		if date1 < start_date or date1 > end_date:
			del data1[i]
		else:
			i = i + 1

	i = 0
	while i < len(data2):
		date2 = datetime.strptime(data2[i][DATE_POS], "%Y-%m-%d")

		# Delete redundant data in dataset1
		if date2 < start_date or date2 > end_date:
			del data2[i]
		else:
			i = i + 1

	return


def test(data1, data2, data1_name, data2_name, data1_price, data2_price, data1_price_name, data2_price_name, start_money, gap_days, trading_day):
	"""
	lundong model test with etf
	"""

	print "Dataset1: %s, data_len=%d, start_date=%s, end_date=%s" % (data1_name, len(data1), data1[0][DATE_POS], data1[-1][DATE_POS])
	print "Dataset2: %s, data_len=%d, start_date=%s, end_date=%s" % (data2_name, len(data2), data2[0][DATE_POS], data2[-1][DATE_POS])
	print "Price1: %s, data_len=%d, start_date=%s, end_date=%s" % (data1_price_name, len(data1_price), data1_price[0][DATE_POS], data1_price[-1][DATE_POS])
	print "Price2: %s, data_len=%d, start_date=%s, end_date=%s" % (data2_price_name, len(data2_price), data2_price[0][DATE_POS], data2_price[-1][DATE_POS])

	# Preprocess datasets
	print "\npreprocessing datasets...\n"
	time_align(data1, data1_price)
	time_align(data2, data2_price)
	time_align(data1, data2)
	time_align(data1, data1_price)
	time_align(data2, data2_price)

	print "Dataset1: %s, data_len=%d, start_date=%s, end_date=%s" % (data1_name, len(data1), data1[0][DATE_POS], data1[-1][DATE_POS])
	print "Dataset2: %s, data_len=%d, start_date=%s, end_date=%s" % (data2_name, len(data2), data2[0][DATE_POS], data2[-1][DATE_POS])
	print "Price1: %s, data_len=%d, start_date=%s, end_date=%s" % (data1_price_name, len(data1_price), data1_price[0][DATE_POS], data1_price[-1][DATE_POS])
	print "Price2: %s, data_len=%d, start_date=%s, end_date=%s" % (data2_price_name, len(data2_price), data2_price[0][DATE_POS], data2_price[-1][DATE_POS])

	# Get close price of two datasets and plot them
	data1_close_price = [ item[CLOSE_PRICE_POS] for item in data1 ]
	data2_close_price = [ item[CLOSE_PRICE_POS] for item in data2 ]
	data1_price_close_price = [ item[CLOSE_PRICE_POS] for item in data1_price ]
	data2_price_close_price = [ item[CLOSE_PRICE_POS] for item in data2_price ]

	analyser = data_analyser()
	analyser.draw_relevance(data1_close_price, data1_price_close_price, data1_name, data1_price_name)
	analyser.draw_relevance(data2_close_price, data2_price_close_price, data2_name, data2_price_name)

	plt.figure(1)
	plt.subplot(311)
	plt.plot(data1_close_price, 'b-', data2_close_price, 'r-')
	plt.legend([data1_name, data2_name], loc="upper left")
	plt.grid(True)

	# Initilize a lundong model, and get trading decisions by it
	lundong_model = lundong()

	# the test start with a blank account
	account = account_simulator(start_money)
	account_real = account_simulator(start_money)
	money = []
	money_real = []

	# record every trading plan
	result = []
	last_valid_trading_plan = {}

	for item in data1:
		trading_plan = lundong_model.get_trading_plan(data1, data2, data1_name, data2_name, item[DATE_POS], gap_days, trading_day, last_valid_trading_plan)

		# if there is a trading plan
		if trading_plan != {}:

			# choise == 0 means buy data1 and sell data2
			if trading_plan["choise"] == 0:

				# fake
				# if we have data2, sell it
				stock = account.get_stock(data2_name)
				if stock != None and stock.share != 0:
					account.sell(data2_name, trading_plan["data2_close_price"], stock.share)

				# buy data1 as many as we can
				account.buy(data1_name, trading_plan["data1_close_price"], int(math.floor(account.money / trading_plan["data1_close_price"])))

				# real
				# if we have data2, sell it
				stock = account_real.get_stock(data2_price_name)
				if stock != None and stock.share != 0:
					real_data = get_data(data2_price, trading_plan["date_str"])
					account_real.sell(data2_price_name, real_data[CLOSE_PRICE_POS], stock.share)

				# buy data1 as many as we can
				real_data = get_data(data1_price, trading_plan["date_str"])
				account_real.buy(data1_price_name, real_data[CLOSE_PRICE_POS], int(math.floor(account_real.money / real_data[CLOSE_PRICE_POS])))

			# choise == 1 means sell data1 and buy data2
			elif trading_plan["choise"] == 1:

				# if we have data1, sell it
				stock = account.get_stock(data1_name)
				if stock != None and stock.share != 0:
					account.sell(data1_name, trading_plan["data1_close_price"], stock.share)

				# buy data2 as many as we can
				account.buy(data2_name, trading_plan["data2_close_price"], int(math.floor(account.money / trading_plan["data2_close_price"])))

				# real
				stock = account_real.get_stock(data1_price_name)
				if stock != None and stock.share != 0:
					real_data = get_data(data1_price, trading_plan["date_str"])
					account_real.sell(data1_price_name, real_data[CLOSE_PRICE_POS], stock.share)

				# buy data1 as many as we can
				real_data = get_data(data2_price, trading_plan["date_str"])
				account_real.buy(data2_price_name, real_data[CLOSE_PRICE_POS], int(math.floor(account_real.money / real_data[CLOSE_PRICE_POS])))

			# choise == 2 means sell all data2
			elif trading_plan["choise"] == 2:

				# if we have data1, sell it
				stock = account.get_stock(data1_name)
				if stock != None and stock.share != 0:
					account.sell(data1_name, trading_plan["data1_close_price"], stock.share)

				# if we have data2, sell it
				stock = account.get_stock(data2_name)
				if stock != None and stock.share != 0:
					account.sell(data2_name, trading_plan["data2_close_price"], stock.share)

				stock = account_real.get_stock(data1_price_name)
				if stock != None and stock.share != 0:
					real_data = get_data(data1_price, trading_plan["date_str"])
					account_real.sell(data1_price_name, real_data[CLOSE_PRICE_POS], stock.share)

				stock = account_real.get_stock(data2_price_name)
				if stock != None and stock.share != 0:
					real_data = get_data(data2_price, trading_plan["date_str"])
					account_real.sell(data2_price_name, real_data[CLOSE_PRICE_POS], stock.share)

			# other choises means do not trade
			else:
				pass
		# if there is no trading plan, do not trade
		else:
			pass

		money.append(account.get_value())
		money_real.append(account_real.get_value())
		#money.append(account.money)
		result.append(trading_plan)

		if trading_plan != {} and trading_plan["choise"] != -1:
			last_valid_trading_plan = trading_plan

	# Get rising rates, choises and plot them
	data1_up = []
	data2_up = []
	choise_0 = []
	choise_0_index = []
	choise_1 = []
	choise_1_index = []
	choise_2 = []
	choise_2_index = []

	i = 0
	for item in result:
		if item == {}:
			data1_up.append(0.0)
			data2_up.append(0.0)
		else:
			data1_up.append(item["data1_up"])
			data2_up.append(item["data2_up"])

			if item["choise"] == 0:
				choise_0.append(item["data1_up"])
				choise_0_index.append(i)
			elif item["choise"] == 1:
				choise_1.append(item["data2_up"])
				choise_1_index.append(i)
			elif item["choise"] == 2:
				choise_2.append(0)
				choise_2_index.append(i)

		i = i + 1

	plt.subplot(312)
	plt.plot(range(len(data1_up)), data1_up, 'b-', range(len(data2_up)), data2_up, 'r-',\
		choise_0_index, choise_0, 'bo', choise_1_index, choise_1, 'ro',\
		choise_2_index, choise_2, 'r^')
	#plt.plot(data1_up, 'b-', data2_up, 'r-', choise_0, 'bo', choise_1, 'r^')
	plt.legend([data1_name, data2_name, "switch to:" + data1_name, "switch to:" + data2_name, "sell all"], loc="upper left")
	plt.grid(True)

	plt.subplot(313)
	plt.plot([item / start_money for item in money], 'g-', \
		[item / start_money for item in money_real], 'k-', \
		[ float(item[CLOSE_PRICE_POS]) / float(data1_price[0][CLOSE_PRICE_POS]) for item in data1_price], 'b-', \
		[ float(item[CLOSE_PRICE_POS]) / float(data2_price[0][CLOSE_PRICE_POS]) for item in data2_price], 'r-')
	plt.legend(["model", "real", data1_price_name, data2_price_name], loc="upper left")
	plt.grid(True)
	#plt.show()

	account.dump()

	return account.get_value() / start_money, account_real.get_value() / start_money

if __name__ == "__main__":

	sh000905_data = load_data("../data/sh000905")
	sh000300_data = load_data("../data/sh000300")

	sh510500_data = load_data("../data/510500")
	sh510300_data = load_data("../data/510300")

	#test(sh000905_data[-200:-1], sh000300_data[-200:-1], "sh000905", "sh000300", 100000)
	#test(sh000905_data[0:1000], sh000300_data[0:1000], "sh000905", "sh000300", 100000)
	gain_rate, gain_rate_real = test(sh000905_data, sh000300_data, "sh000905", "sh000300", sh510500_data, sh510300_data, "sh510500", "sh510300", 100000, 28, 4)

	print gain_rate
	print gain_rate_real
	plt.show()

	"""
	gain_rates = []
	for i in range(0,6):
		result = test(sh000905_data, sh000300_data, "sh000905", "sh000300", 100000, 28, i)
		print "gap_days:", i, " gain_rates:", result
		gain_rates.append(result)

	print gain_rates

	plt.figure(2)
	plt.plot(range(0,6), gain_rates, 'r-')
	plt.show()
	"""

