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

        last_result = self.load_results_from_file("../result/levela_lundong_result")[-1]

        sell_list = []
        buy_list = []

        for item in last_result[1]:
            found_flag = False

            for item2 in result:
                if item["id"] == item2["id"]:
                    found_flag = True

            if not found_flag:
                sell_list.append(item)

        for item in result:
            found_flag = False

            for item2 in last_result[1]:
                if item["id"] == item2["id"]:
                    found_flag = True

            if not found_flag:
                buy_list.append(item)

        final_result = {}
        final_result["result"] = result
        final_result["last_result"] = last_result
        final_result["sell_list"] = sell_list
        final_result["buy_list"] = buy_list

        self.append_result_to_file("../result/levela_lundong_result", result)

        return final_result


    def append_result_to_file(self, filename, result):

        f = open(filename, "a")

        line = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\t"

        for item in result:
            line += str(item["id"])
            line += "|" + str(item["name"])
            line += "|" + str(item["left_year"])
            line += "|" + str(item["price"])
            line += "|" + str(item["profit_rate"])
            line += "|" + str(item["descr"])
            line += "|" + str(item["discount"])
            # line += "|" + str(item[""])
            line += "\t"

        line += "\n"
        f.write(line.encode("utf-8", "ignore"))

        return


    def load_results_from_file(self, filename):

        f = open(filename, "r")

        results = []

        for line in f:
            line = line.strip().decode("utf-8", "ignore")
            ary = line.split("\t")

            date_str = ary[0]

            item_list = []

            for item_str in ary[1:]:
                item = {}

                ary2 = item_str.split("|")

                item["id"] = ary2[0]
                item["name"] = ary2[1]
                item["left_year"] = ary2[2]
                item["price"] = ary2[3]
                item["profit_rate"] = ary2[4]
                item["descr"] = ary2[5]
                item["discount"] = ary2[6]
                item_list.append(item)

            results.append([date_str, item_list])

        return results


    def format_result(self, result):
        delim = "        "

        mail_detail = ""
        mail_detail += "A基金代码" + delim + "A基金名称" + delim + "当前价格" + delim + "修正收益率" + delim + "折价率" + "\n"

        for item in result:
            mail_detail += item["id"] + delim + item["name"] + delim + item["price"] + delim + item["profit_rate"] + delim + item["discount"] + "\n"

        mail_detail += "\n"

        return mail_detail


    def format_html_result(self, result):

        mail_detail = "<p><strong>" + result["last_result"][0] + " 的结果：</strong></p>\n"
        mail_detail += "<table border=\"1\"><tbody>"
        mail_detail += "<tr><td>代码</td><td>名称</td><td>当前价格</td><td>修正收益率</td><td>折价率</td>" + "\n"

        for item in result["last_result"][1]:
            mail_detail += "<tr><td>" + item["id"] + "</td><td>" + item["name"] + "</td><td>" + item["price"] + "</td><td>" + item["profit_rate"] + "</td><td>" + item["discount"] + "</td></tr>\n"

        mail_detail += "</tbody></table>\n"

        mail_detail += "<p><strong>今日结果：</strong></p>\n"
        mail_detail += "<table border=\"1\"><tbody>"
        mail_detail += "<tr><td>代码</td><td>名称</td><td>当前价格</td><td>修正收益率</td><td>折价率</td>" + "\n"

        for item in result["result"]:
            mail_detail += "<tr><td>" + item["id"] + "</td><td>" + item["name"] + "</td><td>" + item["price"] + "</td><td>" + item["profit_rate"] + "</td><td>" + item["discount"] + "</td></tr>\n"

        mail_detail += "</tbody></table>\n"
        
        mail_detail += "<p><strong>建议：</strong></p>\n"

        if len(result["sell_list"]) != 0:
            mail_detail += "<p>卖出："
            for item in result["sell_list"]:
                mail_detail += str(item["name"])
                mail_detail += "、"
            mail_detail += "</p><br/>"

        if len(result["buy_list"]) != 0:
            mail_detail += "<p>买入："
            for item in result["buy_list"]:
                mail_detail += str(item["name"])
                mail_detail += "、"
            mail_detail += "</p><br/>"

        if len(result["sell_list"]) == 0 and len(result["buy_list"]) == 0:
            mail_detail += "<p>保持仓位</p><br/>"

        return mail_detail


if __name__ == '__main__':

    monitor = levela_lundong_monitor()
    result = monitor.monitor(5)

    #monitor.append_result_to_file("./tmp", result)
    #result = monitor.load_results_from_file("./tmp")

    quit()

    if len(result) > 0:

        mail_detail = monitor.format_result(result)

        mail_detail += "\n"
        #mail.sendhtmlmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], "A级基金轮动结果(潘文海)",mail_detail.encode("utf-8", "ignore"))
    
        mail_detail += "naopo我耐你哩~~~" + "\n"
        # mail.sendhtmlmail(['546674175@qq.com', '516563458@qq.com', 'sunada2005@163.com'], "A级基金轮动结果(耐你滴老公~~)",mail_detail.encode("utf-8", "ignore"))
        mail.sendhtmlmail(['sunada2005@163.com'], "A级基金轮动结果(耐你滴老公~~)",mail_detail.encode("utf-8", "ignore"))
        print mail_detail
