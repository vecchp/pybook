from collections import namedtuple
from sortedcontainers import SortedListWithKey
from typing import List
from operator import attrgetter


class PriceUpdate:
    def __init__(self, time=None, type=None, action=None, price=None, quantity=None, order_count=None, level=None):
        self.time = time
        self.type = type
        self.action = action
        self.price = price
        self.quantity = quantity
        self.order_count = order_count
        self.level = level
        self.deleted = False

    def __lt__(self, other):
        return self.price < other.price


Quote = namedtuple('Quote', ['time', 'bid_price', 'bid_quantity', 'ask_price', 'ask_quantity'])


class Book:
    def __init__(self, depth):
        self.depth = depth
        self.empty_price = PriceUpdate("", None, None, None, None, None, None)
        self.orders = SortedListWithKey()

    def update(self, price_update: PriceUpdate) -> bool:
        action = {
            48: self.new_order,
            49: self.update_order,
            50: self.delete_order,
            51: self.delete_thru,
            52: self.delete_from
        }.get(price_update.action, None)

        if action:
            action(price_update)
            return True

        return False

    def update_order(self, price_update: PriceUpdate):
        self.orders[price_update.level-1] = price_update

    def delete_order(self, price_update: PriceUpdate):
        del self.orders[price_update.level-1]

    def delete_thru(self, price_update: PriceUpdate):
        self.orders.clear()

    def new_order(self, price_update: PriceUpdate):
        if len(self.orders) == self.depth:
            self.order.pop()
        self.orders.insert(price_update.level, price_update)

    def get_book(self) -> List[PriceUpdate]:
        return self.orders

    def delete_from(self, price_update: PriceUpdate):
        del self.orders[:price_update.level]

    def top(self) -> PriceUpdate:
        return self.orders[0] if self.orders else self.empty_price


class BidTable(Book):
    def __init__(self, depth):
        super().__init__(depth)
        self.orders = SortedListWithKey(key=lambda price_update: -price_update.price)


class AskTable(Book):
    def __init__(self, depth):
        super().__init__(depth)
        self.orders = SortedListWithKey(key=lambda price_update: price_update.price)


class PyBook:
    def __init__(self, depth):
        self.latest_time = ""
        self.bids = BidTable(depth)
        self.asks = AskTable(depth)
        self.depth = depth

    def update(self, price_update: PriceUpdate) -> bool:
        book = {
            48: self.bids,
            49: self.asks
        }.get(price_update.type, None)

        if book and book.update(price_update):
            self.latest_time = price_update.time
            return True

    def top_of_book(self) -> Quote:
        top_bid = self.bids.top()
        top_ask = self.asks.top()

        return Quote(
            time=self.latest_time,
            bid_price=top_bid.price,
            bid_quantity=top_bid.quantity,
            ask_price=top_ask.price,
            ask_quantity=top_ask.quantity
        )
