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
        no = str(fi.no + 1)
        date = sep[1]
        code = sep[2]
        name = sep[3]
        month_share = sep[4]
        net = sep[5]
        month_amount = sep[6]
        amount_all = -1 * float(fi.sum_month_money) + float(month_amount)
        share = int(fi.share) + int(month_share)

        # print no,date,code,name,net,amount,cost,share
        record = ""
        record += no + '|' + date + '|' + code + '|' + name + '|' + net + '|' + str(month_amount) + '|' + str(amount_all) + '|'
        record += str(month_share) + '|' + str(share) + '|\n'

        # print record
        f = open("../result/intelligent_fixed_investment_result", 'r+')
        content = f.read()
        f.seek(0)
        f.write(record + content)
        f.close()
