#!/usr/bin/env python
#coding: utf-8

import json
import urllib
import time
import sys

def generate_url(page_no):

	return r'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=' + str(page_no) + '&num=80&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page'


def get_page_data(url):

	page = urllib.urlopen(url).read()

	return page


def process_page(data):

	result = []

	ary = data.split('},{')

	for item in ary:
		ary2 = item.split("\"")

		result.append([ary2[1], ary2[5].decode("gbk")])

	return result


def main():
	data_directory = sys.argv[1]

	f = open(data_directory + "/all_stock_data", "w")
	#f = open(cfg.OUTPUT_DIRECTORY + "/all_stock_data", "w")
	stop_flag = False
	i = 1
	stock_num = 0

	while not stop_flag:
		try:
			page_url = generate_url(i)
			page_data = get_page_data(page_url)

			if page_data.strip() == "null":
				stop_flag = True
			else:
				data_list = process_page(page_data)

			for item in data_list:
				print item[0], item[1].encode("utf-8", "ignore")
				f.write(item[0] + "\t" + item[1].replace(' ','').encode("utf-8", "ignore") + "\n")
			
			i = i + 1
			stock_num = stock_num + len(data_list)

		except Exception, ex:
			print ex
			time.sleep(0.5)

	print "Get %d stocks!" % (stock_num)

	f.close()

	return


if __name__ == '__main__':
	main()
