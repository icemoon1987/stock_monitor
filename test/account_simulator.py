#!/usr/bin/env python
#coding=utf-8

class stock_item(object):
    def __init__(self, name):
        self.name = name
        self.mean_price = 0.0
        self.share = 0
        self.value = 0.0
        self.last_op = ""
        self.last_price = 0.0
        self.last_share = 0

        return

class account_simulator(object):
    def __init__(self):
        self.stocks = {}
        return

    def buy(self, name, price, share):

        if name not in self.stocks:
            self.stocks[name] = stock_item(name)

        self.stocks[name].mean_price = (self.stocks[name].value + price * share) / (self.stocks[name].share + share)
        self.stocks[name].share = self.stocks[name].share + share
        self.stocks[name].value = self.stocks[name].mean_price * self.stocks[name].share
        self.stocks[name].last_op = "buy"
        self.stocks[name].last_price = price
        self.stocks[name].last_share = share

        return price * share

    def sell(self, name, share):

        if name not in self.stocks:
            raise

        if self.stocks[name].share < share:
            print "you do not have enough share! name:%s, share:%s, try to sell %d shares!" % (name, self.stocks[name].share, share)
            raise

        self.stocks[name].share = self.stocks[name].share - share
        self.stocks[name].value = self.stocks[name].mean_price * self.stocks[name].share
        self.stocks[name].last_op = "sell"
        self.stocks[name].last_price = self.stocks[name].mean_price
        self.stocks[name].last_share = share

        return share * self.stocks[name].mean_price

    def dump_stock(self, name):
        print "************************************************************************"
        print "stock_name\t\tmean_price\t\tshare\t\tvalue\t\tlast_op\t\tlast_price\t\tlast_share"
        print "%s\t\t%f\t\t%d\t\t%f\t\t%s\t\t%f\t\t%d" % (name, self.stocks[name].mean_price, self.stocks[name].share, self.stocks[name].value, \
            self.stocks[name].last_op, self.stocks[name].last_price, self.stocks[name].last_share)


if __name__ == "__main__":

    account = account_simulator()
    account.buy("sh000001", 100, 10)
    account.dump_stock("sh000001")
    account.buy("sh000001", 50, 10)
    account.dump_stock("sh000001")
    account.sell("sh000001", 15)
    account.dump_stock("sh000001")
    account.sell("sh000001", 5)
    account.dump_stock("sh000001")

    account.sell("sh000001", 1)
    account.dump_stock("sh000001")

