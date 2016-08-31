#!/usr/bin/env python
#coding=utf-8


import sys
sys.path.append("..")

if __name__ == "__main__":
    f = open("turtle_file.txt", "r")
    lines = f.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        sep = line.strip().split('|')
        fi = open("../result/turtle3_result", "r")
        tmp = fi.readline().strip().split('|')
        no = str(int(tmp[0]) + 1)
        fi.close()
        # 第n期|日期|code|名称|买入价格|金额|手续费|份额|操作
        no = sep[0]
        date = sep[1]
        code = sep[2]
        name = sep[3]
        net = sep[4]
        money = str(float(sep[5]) - float(sep[6]) + float(tmp[6]))
        share = str(int(sep[7]) + int(tmp[5]))
        option = sep[8]
        #第n次交易|交易时间|代码|名称|交易价格|交易份额|成本|操作方向
        record = no + "|" + date + "|" + code + "|" + name + "|" + net + "|" + share + "|" + money + "|" + option
        # print record
        fi = open("../result/turtle3_result", "r+")
        content = fi.read()
        fi.seek(0)
        fi.write(record + "\n" + content)
        fi.close()


