#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import mail

from datetime import datetime, timedelta
from data_fetcher.jisilu_fetcher import jisilu_fetcher
from data_interface.stock_dataset import stock_dataset

reload(sys)
sys.setdefaultencoding('utf-8')

class levela_lundong_monitor(object):

	def __init__(self):
		return

	def monitor(self, fund_num):

		result = []

		fetcher = jisilu_fetcher()
		fetch_result = fetcher.get_a_level_fund_list()

		for item in fetch_result:
			if len(result) >= fund_num:
				break

			if item["left_year"] != u"永续":
				continue
			if item["descr"].find(u"无下折") != -1:
				continue

			result.append(item)

		return result

	def format_result(self, result):
		delim = "        "

		mail_detail = ""
		mail_detail += "A基金代码" + delim + "A基金名称" + delim + "当前价格" + delim + "修正收益率" + "\n"

		for item in result:
			mail_detail += item["id"] + delim + item["name"] + delim + item["price"] + delim + item["profit_rate"] + "\n"

		mail_detail += "\n"

		return mail_detail

if __name__ == '__main__':

	monitor = levela_lundong_monitor()
	result = monitor.monitor(5)

	if len(result) > 0:

		mail_detail = monitor.format_result(result)

		mail_detail += "\n"
		#mail.sendmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], "A级基金轮动结果(潘文海)",mail_detail.encode("utf-8", "ignore"))
	
		mail_detail += "naopo我耐你哩~~~" + "\n"
		mail.sendmail(['546674175@qq.com', '516563458@qq.com', 'sunada2005@163.com'], "A级基金轮动结果(耐你滴老公~~)",mail_detail.encode("utf-8", "ignore"))

		print mail_detail
