#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import mail
from data_fetcher.jisilu_fetcher import jisilu_fetcher
from define import premium_rt

reload(sys)
sys.setdefaultencoding('utf-8')

class Kezhuanzhai():
    def monitor(self):
        fetcher = jisilu_fetcher()
        bonds = fetcher.get_kezhuanzhai()
        res = []
        if len(bonds) <= 0:
            return res

        for bond in bonds:
            tmp = float(bond["premium_rt"][:-1])
            if tmp <= premium_rt:
                res.append(bond)
        return res

    def format_html_result(self, bonds):
        detail = "<table border=\"1\"><tbody>"
        detail += "<tr><td>代码</td><td>名称</td><td>当前价格</td><td>溢价率</td><td>税后收益</td>" + "\n"
        if len(bonds) <= 0:
            detail += "暂无机会</br></br>"
            return detail

        for item in bonds:
            detail += "<tr><td>" + item["id"] + "</td><td>" + item["name"] + "</td><td>" + item["price"] + "</td><td>" + item["premium_rt"] + "</td><td>" + item["ytm_rt_tax"] + "</td></tr>\n"

        if detail == "":
            detail += "暂无机会</br></br>"
        else:
            detail = "机会如下：</br>" + detail
        return detail

if __name__ == '__main__':
    mail_detail = "<h3>可转债：</h3>\n\n"

    k = Kezhuanzhai()
    bonds = k.monitor()

    mail_detail += k.format_html_result(bonds)

    mail_detail += "\n"

    # mail.sendhtmlmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], "28轮动结果(潘文海)",mail_detail.encode("utf-8", "ignore"))

    mail_detail += "naopo我耐你哩~~~" + "\n"
    # mail.sendhtmlmail(['546674175@qq.com', '516563458@qq.com', 'sunada2005@163.com'], "轮动模型结果(耐你滴老公)",mail_detail.encode("utf-8", "ignore"))
    mail.sendhtmlmail(['sunada2005@163.com'], "轮动模型结果(耐你滴老公~)", mail_detail.encode("utf-8", "ignore"))
    # print mail_detail