import pytest
#from pybook import PriceUpdate
#from pybook import BidTable, AskTable
from pybook.heapbook import Book, BidUpdate


@pytest.mark.parametrize("ticks,result", [
    ([
         BidUpdate(time=None, action=48, price=9427.00, quantity=40,  order_count=19, level=1),
         BidUpdate(time=None, action=48, price=9426.50, quantity=600, order_count=34, level=2),
         BidUpdate(time=None, action=48, price=9426.00, quantity=850, order_count=25, level=3),
         BidUpdate(time=None, action=48, price=9425.50, quantity=350, order_count=14, level=4),
         BidUpdate(time=None, action=48, price=9425.00, quantity=150, order_count=1,  level=5),
         BidUpdate(time=None, action=49, price=9427.00, quantity=503, order_count=20, level=1),
     ], [
         BidUpdate(time=None, action=49, price=9427.00, quantity=503, order_count=20, level=1),
         BidUpdate(time=None, action=48, price=9426.50, quantity=600, order_count=34, level=2),
         BidUpdate(time=None, action=48, price=9426.00, quantity=850, order_count=25, level=3),
         BidUpdate(time=None, action=48, price=9425.50, quantity=350, order_count=14, level=4),
         BidUpdate(time=None, action=48, price=9425.00, quantity=150, order_count=1, level=5)
    ])

])
def test_update(ticks, result):
    bid_book = Book(5)

    for price_update in ticks:
        bid_book.update(price_update)

    assert result == bid_book.get_book()
