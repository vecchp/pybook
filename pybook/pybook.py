from collections import namedtuple
from sortedcontainers import SortedDict
from typing import List

PriceUpdate = namedtuple("PriceUpdate",
                         ['time', 'type', 'action', 'price', 'quantity', 'order_count', 'level'])

Quote = namedtuple('Quote', ['time', 'bid_price', 'bid_quantity', 'ask_price', 'ask_quantity'])


class Book:
    def __init__(self, depth, multiplier=1):
        self.depth = depth
        self.orders = SortedDict()
        self.empty_price = PriceUpdate("", None, None, None, None, None, None)
        self.multiplier = multiplier

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
        self.orders[self.multiplier * price_update.price] = price_update

    def delete_order(self, price_update: PriceUpdate):
        self.orders.pop(self.multiplier * price_update.price)

    def delete_thru(self, price_update: PriceUpdate):
        self.orders.clear()

    def new_order(self, price_update: PriceUpdate):
        if len(self.orders) == self.depth:
            self.orders.popitem()

        self.orders[self.multiplier * price_update.price] = price_update

    def get_book(self) -> List[PriceUpdate]:
        return self.orders.values()

    def delete_from(self, price_update: PriceUpdate):
        direction = price_update.level
        del self.orders.iloc[:direction]

    def top(self) -> PriceUpdate:
        return self.orders.peekitem(0)[1] if self.orders else self.empty_price


class BidTable(Book):
    def __init__(self, depth):
        super().__init__(depth, -1)


class AskTable(Book):
    def __init__(self, depth):
        super().__init__(depth)


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
