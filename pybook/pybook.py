from pybook.price import PriceUpdate, Quote, BidUpdate, AskUpdate


class PyBook:
    def __init__(self, depth, book):
        self.latest_time = ""
        self.bids = book(depth)
        self.asks = book(depth)
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
