#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import mail
from data_interface.fix_investment_data import fix_investment_data
from data_fetcher.stock_fetcher import stock_fetcher
from define import *
from datetime import datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

class intelligent_fixed_investment_monitor(object):
    def __init__(self):
        self.fi = fix_investment_data()
        return

    # 适合定投日在月末，定投使用
    def calc_money_today(self, code):
        self.fi.get_last_result("../result/intelligent_fixed_investment_result")
        fetcher = stock_fetcher()
        self.fi.net = fetcher.get_present_price(code).close_price
        print "net:" + str(self.fi.net)

        self.fi.code = code
        self.fi.no += 1
        self.fi.date = datetime.now().strftime("%Y-%m-%d")

        new_sum = self.fi.sum_month_money * (1 + EXPE_RATE) + GAP
        #new_sum = self.fi.no * GAP * (1 + EXPE_RATE)
        print "new_sum:",new_sum

        now_sum = self.fi.share * self.fi.net
        print "now_sum:", now_sum

        self.fi.month_money = round(new_sum - now_sum, 6)
        self.fi.month_money = self.fi.month_money if self.fi.month_money < MAX_GAP else MAX_GAP
        self.fi.month_money = self.fi.month_money if self.fi.month_money > (MAX_GAP * -1) else (MAX_GAP * -1)

        print "month_money:" + str(self.fi.month_money)

        share = self.fi.month_money * (1 - DEAL_RATE) / self.fi.net
        self.fi.month_share = round(share, 6)
        self.fi.share += self.fi.month_share

    # 适合定投日在月末，回测使用 不考虑买卖share必须为整百的情况 https://www.jisilu.cn/question/61196
    def calc_money(self, code):
        self.fi.get_last_result("../result/intelligent_fixed_investment_result")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = datetime.strptime(self.fi.date, "%Y-%m-%d") + timedelta(days=5)
        start_date = start_date.strftime("%Y-%m-%d")
        fetcher = stock_fetcher()

        time_arr = start_date.split("-")
        last_key = time_arr[0] + time_arr[1]

        new_dataset = fetcher.get_his_day_k(code, start_date, end_date)
        for item in new_dataset.data:
            time_arr = item.date.split("-")
            key = time_arr[0] + time_arr[1]
            # print "last_key: ", last_key, " key: ", key

            if(key == last_key):
                last_item = item
                continue

            self.fi.code = code
            last_key = key

            self.fi.no += 1
            self.fi.date = last_item.date
            # print "date: ", self.fi.date

            self.fi.net = round(last_item.close_price, 2)
            # print "net: ", self.fi.net

            new_sum = self.fi.sum * (1 + EXPE_RATE) + GAP
            now_sum = self.fi.share * self.fi.net
            self.fi.month_money = round(new_sum - now_sum, 6)
            self.fi.month_money = self.fi.month_money if self.fi.month_money < MAX_GAP else MAX_GAP
            # print "month_money: ", self.fi.month_money

            self.fi.sum_month_money += self.fi.month_money
            self.fi.sum_month_money = round(self.fi.sum_month_money, 6)


            share = self.fi.month_money * (1 - DEAL_RATE) / self.fi.net
            self.fi.month_share = round(share, 6)
            self.fi.share = round(self.fi.share + share, 6)
            # print "share: ", self.fi.share

            self.fi.sum = round(self.fi.net * self.fi.share, 6)

            self.fi.profit = self.fi.sum - self.fi.sum_month_money
            self.fi.profit = round(self.fi.profit, 6)
            # print "profit: ", self.fi.profit

            self.fi.profit_rate = (self.fi.profit / self.fi.sum_month_money) * 100
            self.fi.profit_rate = round(self.fi.profit_rate, 2)
            # print "profit_rate: ", self.fi.profit_rate
            self.recode()

    def recode(self, delim = "|"):
        line = str(self.fi.no) + delim + self.fi.date + delim + self.fi.code + delim + self.fi.name + delim + \
               str(self.fi.net) + delim + str(self.fi.month_money) + delim + str(self.fi.sum_month_money) + delim + \
               str(self.fi.month_share) + delim + str(self.fi.share) + delim + str(self.fi.sum) + delim + \
               str(self.fi.profit) + delim + str(self.fi.profit_rate) + "\n"
        # print "new recode: ", line
        f = open("../result/intelligent_fixed_investment_result", 'r+')
        content = f.read()
        f.seek(0)
        f.write(line + content)
        f.close()
        return

    def format_result(self):
        detail = "第" + str(self.fi.no) + "次定投   " + "\n"
        detail += "定投日：" + str(self.fi.date) + "\n"
        detail += "定投标的：" + str(self.fi.code) + "\n标的名称：" + str(self.fi.name) + "\n\n"
        detail += "定投价格指导价：" + str(self.fi.net) + "\n当期定投份额：" + str(self.fi.month_share) + "\n"
        detail += "当期定投金额：" + str(self.fi.month_money) + "\n\n累计定投额：" + str(self.fi.sum_month_money) + "\n"
        detail += "定投总份额：" + str(self.fi.share) + "\n当月价值：" + str(self.fi.sum_month_money) + "\n"
        detail += "当月收益：" + str(self.fi.profit) + "\n当月收益率：" + str(self.fi.profit_rate)
        return detail

    def format_format_html_result(self):
        detail = ""
        list = ['18','26','27','28','29','30','31']
        tmp = datetime.now().strftime("%d")

        if tmp not in list:
            return "今日为非定投日，定投日安排在月末"
        detail += "<p><font color=red>========================================================== <br/>"
        detail += "Attention! <br/> 月末最后一个交易日可能是今天哦！<br/> Attention! <br/>"
        detail += "==========================================================</font></p>"
        detail += "<p>第" + str(self.fi.no) + "次价值平均法定投" + "<br/>"
        detail += "<p>上次交易日期为：" + str(self.fi.date) + "<br/>"
        detail += "投资标的：" + str(self.fi.code) + " " + str(self.fi.name) + "<br/>"
        detail += "每期定投金额为：" + GAP + "<br/>"
        detail += "建议本次定投金额：" + str(self.fi.month_money)  + "<br/>"
        detail += "建议定投价格：" + str(self.fi.net) + "<br/>"
        detail += "建议本次定投份额：" + str(self.fi.month_share) + "<br/>"
        detail += "累计已定投份额：" + str(self.fi.share) + "</p><br/>"
        return detail

if __name__ == "__main__":
    ifim = intelligent_fixed_investment_monitor()
    # ifim.calc_money("sh510500", "04")   #etf500回测
    # ifim.calc_money("sz399006")       #创业版指数回测
    ifim.calc_money_today("sz159915")   #当天投资指导 创业版etf

    mail.sendhtmlmail(['sunada2005@163.com'], "轮动模型结果(耐你滴老公~)",ifim.format_format_html_result().encode("utf-8", "ignore"))
    # print ifim.format_result()
