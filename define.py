#!/usr/bin/env python
#coding=utf-8

DATE_POS = 0
OPEN_PRICE_POS = 1
HIGH_PRICE_POS = 2
CLOSE_PRICE_POS = 3
LOW_PRICE_POS = 4
VOLUMN_POS = 5

#价值平均法：https://www.jisilu.cn/question/61866  https://www.jisilu.cn/question/61196
GAP = 4000
DEAL_RATE = 0.0002
EXPE_RATE = 0.02
MAX_GAP = 20000  #MAX_GAP为GAP的5倍时回测效果较好；每月定投额应在[-MAX_GAP, MAX_GAP]之间

#以天为交易单位的海龟 2016-9-1
BUY_DAYS = 76
SELL_DAYS = 33

# BUY_DAYS = 60
# SELL_DAYS = 38