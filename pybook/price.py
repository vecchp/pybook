from functools import total_ordering
from collections import namedtuple

Quote = namedtuple('Quote', ['time', 'bid_price', 'bid_quantity', 'ask_price', 'ask_quantity'])


class PriceUpdate:
    def __init__(self, time=None, action=None, price=None, quantity=None, order_count=None, level=None):
        self.time = time
        self.action = action
        self.price = price
        self.quantity = quantity
        self.order_count = order_count
        self.level = level
        self.deleted = False

    def __eq__(self, other):
        return self.time == other.time and \
               self.action == other.action and \
               self.price == other.price and \
               self.quantity == other.quantity and \
               self.order_count == other.order_count and \
               self.level == other.level


@total_ordering
class AskUpdate(PriceUpdate):
    def __lt__(self, other):
        return self.price < other.price


@total_ordering
class BidUpdate(PriceUpdate):
    def __lt__(self, other):
        return self.price > other.price


class CME:
    bid = 48
    ask = 49


def cme_price_maker(time, price_type, action, price, quantity, order_count, level):
    price_update = {
        CME.bid: BidUpdate,
        CME.ask: AskUpdate
    }.get(price_type)

    return price_update(time, action, price, quantity, order_count, level)
