__author__ = 'manda.sun'
import sys
sys.path.append("..")
from data_interface.fix_investment_data import fix_investment_data
from data_fetcher.stock_fetcher import stock_fetcher

if __name__ == '__main__':
    file = open("intelligent_file.txt", "r+")
    for line in file.readlines():
        if line.startswith('#'):
            continue

        fi = fix_investment_data()
        fi.get_last_result("../result/intelligent_fixed_investment_result")
        sep = line.strip().split('|')
        no = sep[0]
        date = sep[1]
        code = sep[2]
        name = sep[3]
        net = sep[4]
        amount = sep[5]
        cost = sep[6]
        month_amount = float(amount) + float(cost)
        amount_all = float(fi.sum_month_money) + month_amount
        month_share = int(sep[7])
        share = int(fi.share) + month_share

        fetcher = stock_fetcher()
        close = fetcher.get_present_price(code).close_price
        now_amount = close * share
        profit = round(now_amount - amount_all, 6)
        profit_rate = round(profit / amount_all,2)

        # print no,date,code,name,net,amount,cost,share
        record = ""
        record += no + '|' + date + '|' + code + '|' + name + '|' + net + '|' + str(month_amount) + '|' + str(amount_all) + '|'
        record += str(month_share) + '|' + str(share) + '|' + str(now_amount) + '|' + str(profit) + '|' + str(profit_rate) + '\n'

        # print record
        f = open("../result/intelligent_fixed_investment_result", 'r+')
        content = f.read()
        f.seek(0)
        f.write(record + content)
        f.close()
