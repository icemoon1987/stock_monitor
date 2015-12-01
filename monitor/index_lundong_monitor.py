#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import mail

from datetime import datetime, timedelta
from data_fetcher.stock_fetcher import stock_fetcher
from data_interface.stock_dataset import stock_dataset

reload(sys)
sys.setdefaultencoding('utf-8')

class index_lundong_monitor(object):

    def __init__(self):
        return

    def monitor(self, days_gap):

        sh000300_his = stock_dataset()
        sh000300_his.load_from_file("sh000300", "../data/sh000300")

        sh000905_his = stock_dataset()
        sh000905_his.load_from_file("sh000905", "../data/sh000905")

        sz399008_his = stock_dataset()
        sz399008_his.load_from_file("sz399008", "../data/sz399008")

        fetcher = stock_fetcher()

        sh000300_now = fetcher.get_present_price("sh000300")
        sh000905_now = fetcher.get_present_price("sh000905")
        sz399008_now = fetcher.get_present_price("sz399008")

        if sh000300_now == None or sh000905_now == None or sz399008_now == None:
            print "get now price error"
            return None

        if sh000300_now.date != sh000905_now.date or sh000300_now.date != sz399008_now.date:
            print "different date"
            return None

        last_valid_date = datetime.strptime(sh000300_his.data[0].date, "%Y-%m-%d")
        now_str = sh000300_now.date
        now = datetime.strptime(now_str, "%Y-%m-%d")
        last = now - timedelta(days=days_gap)

        while True:
            last_str = last.strftime("%Y-%m-%d")

            sh000300_last = sh000300_his.get_data(last_str)
            sh000905_last = sh000905_his.get_data(last_str)
            sz399008_last = sz399008_his.get_data(last_str)

            if sh000300_last != None and sh000905_last != None and sz399008_last:
                break
            else:
                last = last - timedelta(days=1)
                if last < last_valid_date:
                    return None

        sh000300_up = (sh000300_now.close_price - sh000300_last.close_price) / sh000300_last.close_price
        sh000905_up = (sh000905_now.close_price - sh000905_last.close_price) / sh000905_last.close_price
        sz399008_up = (sz399008_now.close_price - sz399008_last.close_price) / sz399008_last.close_price

        result = {}

        result["now_date"] = now_str
        result["last_date"] = last_str
        result["sh000300"] = [sh000300_last.close_price, sh000300_now.close_price, sh000300_up]
        result["sh000905"] = [sh000905_last.close_price, sh000905_now.close_price, sh000905_up]
        result["sz399008"] = [sz399008_last.close_price, sz399008_now.close_price, sz399008_up]

        if sh000300_up > sh000905_up and sh000300_up > sz399008_up:
            result["choise"] = "sh000300"
        elif sh000905_up > sh000300_up and sh000905_up > sz399008_up:
            result["choise"] = "sh000905"
        elif sz399008_up > sh000300_up and sz399008_up > sh000905_up:
            result["choise"] = "sz399008"

        if sh000300_up < 0 and sh000905_up < 0 and sz399008_up < 0:
            result["result"] = "sell all"

        return result

    def format_result(self, result):
        delim = "        "

        mail_detail = ""
        mail_detail += "市场类型" + delim + "指数名称" + delim + "指数代码" + delim + "四周前指数" + delim + "当前指数" + delim + "涨幅" + delim + "投资工具" + "\n"
        mail_detail += "权重盘" + delim + "沪深300" + delim + "sh000300" + delim + str(result["sh000300"][0]) + delim + str(result["sh000300"][1]) + \
                      delim + str(int(result["sh000300"][2] * 10000) / 100.0 ) + "%" + delim + "华泰柏瑞沪深300ETF(510300)、广发沪深300(270010)" + "\n"
        mail_detail += "中小盘" + delim + "中证小盘500" + delim + "sh000905" + delim + str(result["sh000905"][0]) + delim + str(result["sh000905"][1]) + \
                      delim + str(int(result["sh000905"][2] * 10000) / 100.0 ) + "%" + delim + "南方中证500ETF(510500)" + "\n"
        mail_detail += "中小盘" + delim + "中小板300" + delim + "sz399008" + delim + str(result["sz399008"][0]) + delim + str(result["sz399008"][1]) + \
                      delim + str(int(result["sz399008"][2] * 10000) / 100.0 ) + "%" + delim + "广发中小板300联(270026)" + "\n"
        mail_detail += "\n"
        mail_detail += "建议： "

        if result["choise"] == "sh000300":
            mail_detail += "轮动到 沪深300 的投资工具"
        elif result["choise"] == "sh000905":
            mail_detail += "轮动到 中证小盘500 的投资工具"
        elif result["choise"] == "sz399008":
            mail_detail += "轮动到 中小板300 的投资工具"
        elif result["choise"] == "sell all":
            mail_detail += "清仓"

        mail_detail += "\n"

        return mail_detail


    def format_html_result(self, result):

        mail_detail = "<table border=\"1\"><tbody>"
        mail_detail += "<tr><td>类型</td><td>名称</td><td>代码</td><td>四周前</td><td>当前</td><td>涨跌幅</td><td>工具</td></tr>\n"

        color = "green"
        if result["sh000300"][2] > 0:
            color = "red"

        mail_detail += "<tr><td>权重</td><td>沪深300</td><td>sh000300</td><td>" + str(result["sh000300"][0]) + "</td><td>" + str(result["sh000300"][1]) + "</td><td><span style=\"color: " + color + ";\">" + str(int(result["sh000300"][2] * 10000) / 100.0 ) + "%" + "</span></td>" + "<td>华泰柏瑞沪深300ETF(510300)、广发沪深300(270010)</td>\n"

        color = "green"
        if result["sh000905"][2] > 0:
            color = "red"

        mail_detail += "<tr><td>中小</td><td>中小盘500</td><td>sh000905</td><td>" + str(result["sh000905"][0]) + "</td><td>" + str(result["sh000905"][1]) + "</td><td><span style=\"color: " + color + ";\">" + str(int(result["sh000905"][2] * 10000) / 100.0 ) + "%" + "</span></td>" + "<td>南方中证500ETF(510500)</td>\n"

        color = "green"
        if result["sz399008"][2] > 0:
            color = "red"

        mail_detail += "<tr><td>中小</td><td>中小板300</td><td>sz399008</td><td>" + str(result["sz399008"][0]) + "</td><td>" + str(result["sz399008"][1]) + "</td><td><span style=\"color: " + color + ";\">" + str(int(result["sz399008"][2] * 10000) / 100.0 ) + "%" + "</span></td>" + "<td>广发中小板300联(270026)</td>\n"

        mail_detail += "</tbody></table>\n"

        mail_detail += "<p><strong>建议： "

        if result["choise"] == "sh000300":
            mail_detail += "轮动到 沪深300 的工具"
        elif result["choise"] == "sh000905":
            mail_detail += "轮动到 中证小盘500 的工具"
        elif result["choise"] == "sz399008":
            mail_detail += "轮动到 中小板300 的工具"
        elif result["choise"] == "sell all":
            mail_detail += "清仓"

        mail_detail += "</strong></p>\n"

        return mail_detail

if __name__ == '__main__':

    monitor = index_lundong_monitor()
    result = monitor.monitor(27)

    mail_detail = monitor.format_result(result)

    mail_detail += "\n"
    mail.sendmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], "28轮动结果(潘文海)",mail_detail.encode("utf-8", "ignore"))
    
    mail_detail += "naopo我耐你哩~~~" + "\n"
    mail.sendmail(['546674175@qq.com', '516563458@qq.com', 'sunada2005@163.com'], "28轮动结果(耐你滴老公~~)",mail_detail.encode("utf-8", "ignore"))

    print mail_detail

