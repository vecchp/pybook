import pytest
from pybook import PriceUpdate
from pybook import BidTable, AskTable

bid_1_results = [
    PriceUpdate(time=None, type=48, action=48, price=9427.00, quantity=503, order_count=20, level=1),
    PriceUpdate(time=None, type=48, action=48, price=9426.50, quantity=750, order_count=34, level=2),
    PriceUpdate(time=None, type=48, action=48, price=9426.00, quantity=400, order_count=25, level=3),
    PriceUpdate(time=None, type=48, action=48, price=9425.50, quantity=300, order_count=14, level=4),
    PriceUpdate(time=None, type=48, action=48, price=9425.00, quantity=400, order_count=1, level=5),
]

ask_1_results = [
    PriceUpdate(time=None, type=49, action=48, price=9428.00, quantity=40, order_count=2, level=1),
    PriceUpdate(time=None, type=49, action=48, price=9428.50, quantity=600, order_count=35, level=2),
    PriceUpdate(time=None, type=49, action=48, price=9429.00, quantity=850, order_count=55, level=3),
    PriceUpdate(time=None, type=49, action=48, price=9429.50, quantity=350, order_count=21, level=4),
    PriceUpdate(time=None, type=49, action=48, price=9430.00, quantity=150, order_count=12, level=5),
]


@pytest.mark.parametrize("ticks,book_type,result", [
    (bid_1_results, BidTable, bid_1_results),
    ([
         PriceUpdate(time=None, type=48, action=48, price=9425.50, quantity=300, order_count=14, level=4),
         PriceUpdate(time=None, type=48, action=48, price=9425.00, quantity=400, order_count=1, level=5),
         PriceUpdate(time=None, type=48, action=48, price=9426.50, quantity=750, order_count=34, level=2),
         PriceUpdate(time=None, type=48, action=48, price=9427.00, quantity=503, order_count=20, level=1),
         PriceUpdate(time=None, type=48, action=48, price=9426.00, quantity=400, order_count=25, level=3),
     ], BidTable, bid_1_results),
    (ask_1_results, AskTable, ask_1_results),
    ([
        PriceUpdate(time=None, type=49, action=48, price=9428.00, quantity=40, order_count=2, level=1),
        PriceUpdate(time=None, type=49, action=48, price=9430.00, quantity=150, order_count=12, level=5),
        PriceUpdate(time=None, type=49, action=48, price=9428.50, quantity=600, order_count=35, level=2),
        PriceUpdate(time=None, type=49, action=48, price=9429.50, quantity=350, order_count=21, level=4),
        PriceUpdate(time=None, type=49, action=48, price=9429.00, quantity=850, order_count=55, level=3)
    ], AskTable, ask_1_results)
])
def test_bid_book(ticks, book_type, result):
    bid_book = book_type(5)

    for price_update in ticks:
        bid_book.update(price_update)

    for expected, actual in zip(result, bid_book.get_book()):
        assert expected == actual


