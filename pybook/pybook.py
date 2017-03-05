from collections import namedtuple
from sortedcontainers import SortedDict

PriceUpdate = namedtuple("price_update", ['type', 'action', 'price', 'quantity', 'order_count', 'level'])


class Book:
    def __init__(self, depth):
        self.depth = depth
        self.orders = SortedDict()

    def update(self, price_update: PriceUpdate):
        action = {
            '0': self.new_order,
            '1': self.update_order,
            '2': self.delete_order,
            '3': self.delete_thru,
            '4': self.delete_from
        }[price_update.action]

        action(price_update)

    def update_order(self, price_update: PriceUpdate):
        self.orders[price_update.price] = price_update

    def delete_order(self, price_update: PriceUpdate):
        self.orders.pop(price_update.price)

    def delete_thru(self, price_update: PriceUpdate):
        self.orders.clear()


class BidTable(Book):
    def new_order(self, price_update: PriceUpdate):
        self.orders[price_update.price] = price_update

        if len(self.orders) > self.depth:
            self.orders.popitem(last=True)

    def get_book(self):
        return reversed(self.orders.values())

    def delete_from(self, price_update: PriceUpdate):
        direction = price_update.level - 1
        del self.orders.iloc[:-direction]

    def top(self):
        return self.orders.peekitem(-1)


class AskTable(Book):
    def new_order(self, price_update: PriceUpdate):
        self.orders[price_update.price] = price_update
        if len(self.orders) > self.depth:
            self.orders.popitem()

    def get_book(self):
        return self.orders.values()

    def delete_from(self, price_update: PriceUpdate):
        direction = price_update.level
        del self.orders.iloc[:direction]

    def top(self):
        return self.orders.peekitem(0)


class PyBook:
    def __init__(self, depth):
        self.bids = BidTable(depth)
        self.asks = AskTable(depth)
        self.depth = depth

    def update(self, price_update: PriceUpdate):
        book = {
            '0': self.bids,
            '1': self.asks
        }[price_update.type]

        book.update(price_update)
