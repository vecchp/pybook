import pytest
from pybook import PriceUpdate
from pybook import BidTable, AskTable


@pytest.mark.parametrize("ticks,book_type,result", [
    ([
         PriceUpdate(type='0', action='0', price=9427.00, quantity=40,  order_count=19, level=1),
         PriceUpdate(type='0', action='0', price=9426.50, quantity=600, order_count=34, level=2),
         PriceUpdate(type='0', action='0', price=9426.00, quantity=850, order_count=25, level=3),
         PriceUpdate(type='0', action='0', price=9425.50, quantity=350, order_count=14, level=4),
         PriceUpdate(type='0', action='0', price=9425.00, quantity=150, order_count=1,  level=5),
         PriceUpdate(type='0', action='1', price=9427.00, quantity=503, order_count=20, level=None),
     ], BidTable, [
         PriceUpdate(type='0', action='1', price=9427.00, quantity=503, order_count=20, level=None),
         PriceUpdate(type='0', action='0', price=9426.50, quantity=600, order_count=34, level=2),
         PriceUpdate(type='0', action='0', price=9426.00, quantity=850, order_count=25, level=3),
         PriceUpdate(type='0', action='0', price=9425.50, quantity=350, order_count=14, level=4),
         PriceUpdate(type='0', action='0', price=9425.00, quantity=150, order_count=1, level=5)
    ])

])
def test_update(ticks, book_type, result):
    bid_book = book_type(5)

    for price_update in ticks:
        bid_book.update(price_update)

    for i, price in enumerate(bid_book.get_book()):
        assert (result[i] == price)
