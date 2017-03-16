from collections import namedtuple
from heapq import heappush, heappop
from typing import List
from functools import total_ordering


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


Quote = namedtuple('Quote', ['time', 'bid_price', 'bid_quantity', 'ask_price', 'ask_quantity'])


def cme_price_maker(time, price_type, action, price, quantity, order_count, level):
    price_update = {
        CME.bid: BidUpdate,
        CME.ask: AskUpdate
    }.get(price_type)

    return price_update(time, action, price, quantity, order_count, level)


class Book:
    def __init__(self, depth):
        self.depth = depth
        self.orders_heap = []
        self.order_map = {}
        self.empty_price = PriceUpdate()

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

        existing_price = self.order_map.get(price_update.price)

        if existing_price:
            existing_price.deleted = True

        heappush(self.orders_heap, price_update)
        self.order_map[price_update.price] = price_update

    def delete_order(self, price_update: PriceUpdate):
        existing_price = self.order_map.get(price_update.price)
        existing_price.deleted = True

    def delete_thru(self, price_update: PriceUpdate):
        self.orders_heap = []
        self.order_map = {}

    def new_order(self, price_update: PriceUpdate):
        if len(self.order_map) == self.depth:
            while self.orders_heap and self.orders_heap[0].deleted:
                heappop(self.orders_heap)
                self.order_map.pop(price_update.price)

        self.order_map[price_update.price] = price_update
        heappush(self.orders_heap, price_update)

    def get_book(self) -> List[PriceUpdate]:
        return sorted((pu for pu in self.orders_heap if not pu.deleted))

    def delete_from(self, price_update: PriceUpdate):
        num_deleted = 0
        while num_deleted < price_update.level and self.orders_heap:
            top_of_book = heappop(self.orders_heap)
            if not top_of_book.deleted:
                num_deleted += 1
                self.order_map.pop(top_of_book.price)

    def top(self) -> PriceUpdate:
        return self.orders_heap[0] if self.order_heap else self.empty_price


class PyBook:
    def __init__(self, depth):
        self.latest_time = ""
        self.bids = Book(depth)
        self.asks = Book(depth)
        self.depth = depth

    def update(self, price_update: PriceUpdate) -> bool:
        if isinstance(price_update, BidUpdate):
            self.bids.update(price_update)
        elif isinstance(price_update, AskUpdate):
            self.asks.update(price_update)

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
