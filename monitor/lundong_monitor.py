#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import mail
from datetime import datetime, timedelta
from index_lundong_monitor import index_lundong_monitor
from levela_lundong_monitor import levela_lundong_monitor
from intelligent_fixed_investment_monitor import  intelligent_fixed_investment_monitor
from turtle_monitor import turtle_monitor

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

    mail_detail = "<h3>1、28指数轮动模型结果（广发基金账户）：</h3>"

    index_monitor = index_lundong_monitor()
    result = index_monitor.monitor(27)
    mail_detail += index_monitor.format_html_result(result)
    mail_detail += "\n"

    mail_detail += "<h3>2、分级A轮动模型结果（01证券账户）：</h3>"
    levela_monitor = levela_lundong_monitor()
    result = levela_monitor.monitor(5)
    mail_detail += levela_monitor.format_html_result(result)

    mail_detail += "<h3>3、价值平均法定投（01证券账户）:</h3>"
    intelligent = intelligent_fixed_investment_monitor()
    intelligent.calc_money_today("sz159915")
    mail_detail += intelligent.format_format_html_result()

    mail_detail += "<h3>4、沪深300海龟轮动（01证券账户）：</h3>"
    tmonitor = turtle_monitor()
    code = "sh000300"  #沪深300
    result = tmonitor.monitor(code)
    mail_detail += tmonitor.format_format_result(result)
    # mail.sendhtmlmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], "轮动模型结果(潘文海)",mail_detail.encode("utf-8", "ignore"))

    mail.sendhtmlmail(['546674175@qq.com', '516563458@qq.com', 'sunada2005@163.com'], "轮动模型结果(耐你滴老公)",mail_detail.encode("utf-8", "ignore"))

    # mail.sendhtmlmail(['sunada2005@163.com'], "轮动模型结果(耐你滴老公~)",mail_detail.encode("utf-8", "ignore"))

    # print mail_detail
