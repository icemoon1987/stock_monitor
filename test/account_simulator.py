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
    def __init__(self, money):
        self.stocks = {}
        self.money = money
        return

    def buy(self, name, price, share):

        if name not in self.stocks:
            self.stocks[name] = stock_item(name)

        if (price * share) > self.money:
            print "not enough money! money:%f, try_to_spend:%f" % (self.money, price*share)
            raise

        self.stocks[name].mean_price = (self.stocks[name].value + price * share) / (self.stocks[name].share + share)
        self.stocks[name].share = self.stocks[name].share + share
        self.stocks[name].value = self.stocks[name].mean_price * self.stocks[name].share
        self.stocks[name].last_op = "buy"
        self.stocks[name].last_price = price
        self.stocks[name].last_share = share
        self.money = self.money - (share * price)

        return price * share

    def sell(self, name, price, share):

        if name not in self.stocks:
            raise

        if self.stocks[name].share < share:
            print "you do not have enough share! name:%s, share:%s, try to sell %d shares!" % (name, self.stocks[name].share, share)
            raise

        self.stocks[name].share = self.stocks[name].share - share
        self.stocks[name].value = self.stocks[name].mean_price * self.stocks[name].share
        self.stocks[name].last_op = "sell"
        self.stocks[name].last_price = price
        self.stocks[name].last_share = share
        self.money = self.money + (share * price)

        return price * share

    def get_stock(self, name):

        if name in self.stocks:
            return self.stocks[name]

        return None

    def get_money(self):
        return self.money

    def get_value(self):

        result = 0.0

        for name in self.stocks:
            result = result + self.stocks[name].value

        result = result + self.money

        return result

    def dump_stock(self, name):
        print "*****************************************************************************************************"
        print "stock_name\t\tmean_price\t\tshare\t\tvalue\t\tlast_op\t\tlast_price\t\tlast_share"
        print "%s\t\t%f\t\t%d\t\t%f\t\t%s\t\t%f\t\t%d" % (name, self.stocks[name].mean_price, self.stocks[name].share, self.stocks[name].value, \
            self.stocks[name].last_op, self.stocks[name].last_price, self.stocks[name].last_share)
        print ""

        return

    def dump(self):
        print "*****************************************************************************************************"
        print "stock_name\t\tmean_price\t\tshare\t\tvalue\t\tlast_op\t\tlast_price\t\tlast_share"

        for name in self.stocks:
            print "%s\t\t%f\t\t%d\t\t%f\t\t%s\t\t%f\t\t%d" % (name, self.stocks[name].mean_price, self.stocks[name].share, self.stocks[name].value, \
                self.stocks[name].last_op, self.stocks[name].last_price, self.stocks[name].last_share)
        print "remain money: %f" % (self.money)
        print ""


        return

if __name__ == "__main__":

    cost = 0.0
    gain = 0.0

    account = account_simulator(10000)
    cost = cost + account.buy("sh000001", 100, 10)
    account.dump()
    cost = cost + account.buy("sh000001", 50, 10)
    account.dump()
    gain = gain + account.sell("sh000001", 20, 15)
    account.dump()
    gain = gain + account.sell("sh000001", 1000, 5)
    account.dump()

    account.buy("sh000009", 10.02, 45)
    account.buy("sh000010", 10.02, 45)
    account.buy("sh000009", 10.02, 45)
    account.buy("sh000010", 10.02, 45)
    account.buy("sh000010", 10.02, 4500000)

    account.dump()

    print cost, gain, gain - cost

