#!/usr/bin/env python
#coding=utf-8

import urllib
import myjson
from  datetime  import  *  
import  time 

class 28lundong(object):

	def get_closing_date(self, id, given_day):
		str_given_day = given_day.strftime("%Y%m%d")
		#print str_given_day
		url = 'http://q.stock.sohu.com/hisHq?code=' + id + '&start=' + str_given_day + '&end=' + str_given_day + '&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp'
		#print url
		data = urllib.urlopen(url).read()
		content = data.split('(')[1].split(')')[0]
		content_data = myjson.read(content)
		if content_data == {}:
			given_day = given_day - timedelta(days = 1)
			#print given_day
			given_day = get_closing_date(id, given_day)
		return given_day

	def get_his_price(self, id, given_day):
		str_given_day = given_day.strftime("%Y%m%d")
		url = 'http://q.stock.sohu.com/hisHq?code=' + id + '&start=' + str_given_day + '&end=' + str_given_day + '&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp'
		#print url
		data = urllib.urlopen(url).read()
		#print data
		content = data.split('(')[1].split(')')[0]
		#print 'content:', content
		#print
		content_data = myjson.read(content)
		#print 'content_data:',content_data
		#print
		
		#print 'wanted:', content_data[0]['hq']
		#print
		return content_data[0]['hq'][0][2]

	def get_realtime_price(self, id):
		url = 'http://hq.sinajs.cn/list=' + id
		#print url
		data = urllib.urlopen(url).read()
		#print "new price: ", data
		return data.split(',')[3]

	def get_ups(id1_sina, id2_sina, id1_sohu, id2_sohu):
		#today = date.today() + timedelta(days = 1)
		today = date.today()
		print "Today is: ", today
		
		"""
		#last trading day price
		new_price1 = float(get_price(id1, last_trading_day))
		new_price2 = float(get_price(id2, last_trading_day))
		print "last trading date: ", last_trading_day
		print "last closing price: ", id1, new_price1
		print "last closing price: ", id2, new_price2
		"""

		#real time price
		new_price1 = float(get_realtime_price(id1_sina))
		new_price2 = float(get_realtime_price(id2_sina))
		print 'Now the price: ', id1_sina, new_price1
		print 'Now the price: ', id2_sina, new_price2

		last_trading_day = get_closing_date(id1_sohu, today)
		four_weeks_ago = last_trading_day - timedelta(days = 27)
		print "4 weeks ago: ", four_weeks_ago
		day = get_closing_date(id1_sohu, four_weeks_ago)
		old_price1 = float(get_his_price(id1_sohu, day))
		old_price2 = float(get_his_price(id2_sohu, day))
		print "The lastest four week trading day: ", day
		print "That day's closing price: ", id1_sohu, old_price1
		print "That day's closing price: ", id2_sohu, old_price2

		up1 = (new_price1 - old_price1) / old_price1 * 100
		up2 = (new_price2 - old_price2) / old_price2 * 100
		print id1_sina, 'up:', up1, "%"
		print id2_sina, 'up:', up2, "%"
		return up1, up2



if __name__ == '__main__':
	"""
	#etf500_sohu = 'cn_510500'
	#etf300_sohu = 'cn_510300'
	"""
	etf500_sohu = 'zs_000905'
	etf300_sohu = 'zs_000300'
	
	etf300_sina = 'sh000300'
	etf500_sina = 'sh000905'
	up500, up300 = get_ups(etf500_sina, etf300_sina,etf500_sohu, etf300_sohu)

	if up500 > up300:
		print "Buy 500etf (510500)"
	elif up500 < up300:
		print "Buy 300etf (510300)"
	else:
		print "up500 == up300"


