from heapq import heappush, heappop
from typing import List
from pybook.price import PriceUpdate


class HeapBook:
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