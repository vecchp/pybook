from sortedcontainers import SortedDict
from typing import List
from pybook.pybook import PriceUpdate


class SortedDictBook:
    def __init__(self, depth):
        self.depth = depth
        self.orders = SortedDict()
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
        self.orders[price_update.price] = price_update

    def delete_order(self, price_update: PriceUpdate):
        self.orders.pop(price_update.price)

    def delete_thru(self, price_update: PriceUpdate):
        self.orders.clear()

    def new_order(self, price_update: PriceUpdate):
        if len(self.orders) == self.depth:
            self.orders.popitem()

        self.orders[price_update.price] = price_update

    def get_book(self) -> List[PriceUpdate]:
        return self.orders.values()

    def delete_from(self, price_update: PriceUpdate):
        direction = price_update.level
        del self.orders.iloc[:direction]

    def top(self) -> PriceUpdate:
        return self.orders.peekitem(0)[1] if self.orders else self.empty_price
