#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import mail
from datetime import datetime, timedelta
from index_lundong_monitor import index_lundong_monitor
from levela_lundong_monitor import levela_lundong_monitor

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

	mail_detail = "<h3>指数轮动模型结果：</h3>\n\n"

	index_monitor = index_lundong_monitor()
	result = index_monitor.monitor(27)
	mail_detail += index_monitor.format_html_result(result)

	mail_detail += "\n"

	# mail_detail += "<h3>分级A轮动模型结果：</h3>\n\n"
	# levela_monitor = levela_lundong_monitor()
	# result = levela_monitor.monitor(5)
	# mail_detail += levela_monitor.format_html_result(result)
    #
	# mail_detail += "\n"

	# mail.sendhtmlmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], "轮动模型结果(潘文海)",mail_detail.encode("utf-8", "ignore"))

	mail.sendhtmlmail(['546674175@qq.com', '516563458@qq.com', 'sunada2005@163.com'], "轮动模型结果(耐你滴老公)",mail_detail.encode("utf-8", "ignore"))

	# mail.sendhtmlmail(['sunada2005@163.com'], "轮动模型结果(耐你滴老公~)",mail_detail.encode("utf-8", "ignore"))

	print mail_detail
