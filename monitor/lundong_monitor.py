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
from small_market_value_monitor import small_market_value_monitor
from dividents_monitor import Dividents_monitor
import logging
import os

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename='lundong.log',
                        filemode='w')

    logging.debug("Lundong Start.")
    mail_detail = ""

    mail_detail += "<h3>1、价值平均法定投（01证券账户）:</h3>"
    intelligent = intelligent_fixed_investment_monitor()
    intelligent.calc_money_today("sz159915")
    mail_detail += intelligent.format_format_html_result()
    mail_detail += "\n红利ETF & H股ETF（3k）可同一天定投\n"
    logging.debug("intelligent_fixed_investment_monitor runs successfully!")

    mail_detail += "<h3>2、小市值轮动换仓建议(2w)：</h3>"
    smvm = small_market_value_monitor()
    try:
        mail_detail += smvm.format_format_html_result()
    except Exception, ex:
        logging.debug(str(ex))
    logging.debug("small_market_value_monitor runs successfully!")

    mail_detail += "<h3>3、红利股轮动(5w)：</h3>"
    mail_detail_from_file = ""
    with open("dividents_monitor_result", 'r') as fr:
        mail_detail_from_file = fr.readline()
    mail_detail += mail_detail_from_file
    logging.debug("Dividents_monitor runs successfully!")

    mail_detail += "<h3>4、28指数轮动模型结果（广发基金账户）：</h3>"
    index_monitor = index_lundong_monitor()
    result = index_monitor.monitor(27)
    mail_detail += index_monitor.format_html_result(result)
    mail_detail += "\n"
    logging.debug("index_lundong_monitor runs successfully!")

    mail_detail += "<h3>5、分级A轮动模型结果（01证券账户）：</h3>"
    levela_monitor = levela_lundong_monitor()
    result = levela_monitor.monitor(5)
    mail_detail += levela_monitor.format_html_result(result)
    logging.debug("levela_lundong_monitor runs successfully!")

    mail_detail += "<h3>6、沪深300海龟轮动（01证券账户）：</h3>"
    tmonitor = turtle_monitor()
    code = "sh000300"  #沪深300
    result = tmonitor.monitor(code)
    mail_detail += tmonitor.format_format_result(result)
    logging.debug("turtle_monitor runs successfully!")
    # mail.sendhtmlmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], "轮动模型结果(潘文海)",mail_detail.encode("utf-8", "ignore"))

    #mail.sendhtmlmail(['546674175@qq.com', '516563458@qq.com', 'sunada2005@163.com'], "轮动模型结果(耐你滴老公)",mail_detail.encode("utf-8", "ignore"))
    # print mail_detail
    mail.sendhtmlmail(['sunada2005@163.com','516563458@qq.com'], "轮动模型结果(耐你滴老公~)",mail_detail.encode("utf-8", "ignore"))

    # print mail_detail
