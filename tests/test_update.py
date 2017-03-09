import pytest
from pybook import PriceUpdate
from pybook import BidTable, AskTable


@pytest.mark.parametrize("ticks,book_type,result", [
    ([
         PriceUpdate(time=None, type=48, action=48, price=9427.00, quantity=40,  order_count=19, level=1),
         PriceUpdate(time=None, type=48, action=48, price=9426.50, quantity=600, order_count=34, level=2),
         PriceUpdate(time=None, type=48, action=48, price=9426.00, quantity=850, order_count=25, level=3),
         PriceUpdate(time=None, type=48, action=48, price=9425.50, quantity=350, order_count=14, level=4),
         PriceUpdate(time=None, type=48, action=48, price=9425.00, quantity=150, order_count=1,  level=5),
         PriceUpdate(time=None, type=48, action=49, price=9427.00, quantity=503, order_count=20, level=None),
     ], BidTable, [
         PriceUpdate(time=None, type=48, action=49, price=9427.00, quantity=503, order_count=20, level=None),
         PriceUpdate(time=None, type=48, action=48, price=9426.50, quantity=600, order_count=34, level=2),
         PriceUpdate(time=None, type=48, action=48, price=9426.00, quantity=850, order_count=25, level=3),
         PriceUpdate(time=None, type=48, action=48, price=9425.50, quantity=350, order_count=14, level=4),
         PriceUpdate(time=None, type=48, action=48, price=9425.00, quantity=150, order_count=1, level=5)
    ])

])
def test_update(ticks, book_type, result):
    bid_book = book_type(5)

    for price_update in ticks:
        bid_book.update(price_update)

    for expected, actual in zip(result, bid_book.get_book()):
        assert expected == actual

