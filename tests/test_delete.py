import pytest
from pybook import PriceUpdate
from pybook import BidTable, AskTable


@pytest.mark.parametrize("ticks,book_type,result", [
    ([
         PriceUpdate(type='0', action='0', price=9425.50, quantity=300, order_count=14, level=4),
         PriceUpdate(type='0', action='0', price=9425.00, quantity=400, order_count=1, level=5),
         PriceUpdate(type='0', action='0', price=9426.50, quantity=750, order_count=34, level=2),
         PriceUpdate(type='0', action='0', price=9427.00, quantity=503, order_count=20, level=1),
         PriceUpdate(type='0', action='0', price=9426.00, quantity=400, order_count=25, level=3),
         PriceUpdate(type='0', action='3', price=None, quantity=None, order_count=None, level=3),
     ], BidTable, []),
    ([
         PriceUpdate(type='1', action='0', price=9428.00, quantity=40, order_count=2, level=1),
         PriceUpdate(type='1', action='0', price=9430.00, quantity=150, order_count=12, level=5),
         PriceUpdate(type='1', action='0', price=9428.50, quantity=600, order_count=35, level=2),
         PriceUpdate(type='1', action='0', price=9429.50, quantity=350, order_count=21, level=4),
         PriceUpdate(type='1', action='3', price=None, quantity=None, order_count=None, level=3),
     ], AskTable, [])
])
def test_delete_thru(ticks, book_type, result):
    bid_book = book_type(5)

    for price_update in ticks:
        bid_book.update(price_update)

    for i, price in enumerate(bid_book.get_book()):
        assert (result[i] == price)


@pytest.mark.parametrize("ticks,book_type,result", [
    ([
         PriceUpdate(type='1', action='0', price=9428.00, quantity=40, order_count=2, level=1),
         PriceUpdate(type='1', action='0', price=9428.50, quantity=600, order_count=35, level=2),
         PriceUpdate(type='1', action='0', price=9429.00, quantity=850, order_count=55, level=3),
         PriceUpdate(type='1', action='0', price=9429.50, quantity=350, order_count=21, level=4),
         PriceUpdate(type='1', action='0', price=9430.00, quantity=150, order_count=12, level=5),
         PriceUpdate(type='1', action='4', price=None, quantity=None, order_count=None, level=3),
     ], AskTable, [
         PriceUpdate(type='1', action='0', price=9429.50, quantity=350, order_count=21, level=4),
         PriceUpdate(type='1', action='0', price=9430.00, quantity=150, order_count=12, level=5)
     ]),
    ([
         PriceUpdate(type='0', action='0', price=9428.00, quantity=503, order_count=20, level=1),
         PriceUpdate(type='0', action='0', price=9428.50, quantity=750, order_count=34, level=2),
         PriceUpdate(type='0', action='0', price=9429.00, quantity=400, order_count=25, level=3),
         PriceUpdate(type='0', action='0', price=9429.50, quantity=300, order_count=14, level=4),
         PriceUpdate(type='0', action='0', price=9430.00, quantity=400, order_count=1, level=5),
         PriceUpdate(type='0', action='4', price=None, quantity=None, order_count=None, level=3),
     ], BidTable, [
         PriceUpdate(type='0', action='0', price=9430.00, quantity=400, order_count=1, level=5),
         PriceUpdate(type='0', action='0', price=9429.50, quantity=300, order_count=14, level=4)
     ])

])
def test_delete_from(ticks, book_type, result):
    bid_book = book_type(5)

    for price_update in ticks:
        bid_book.update(price_update)

    for i, price in enumerate(bid_book.get_book()):
        assert (result[i] == price)


@pytest.mark.parametrize("ticks,book_type,result", [
    ([
         PriceUpdate(type='1', action='0', price=9428.00, quantity=40, order_count=2, level=1),
         PriceUpdate(type='1', action='0', price=9428.50, quantity=600, order_count=35, level=2),
         PriceUpdate(type='1', action='0', price=9429.00, quantity=850, order_count=55, level=3),
         PriceUpdate(type='1', action='0', price=9429.50, quantity=350, order_count=21, level=4),
         PriceUpdate(type='1', action='0', price=9430.00, quantity=150, order_count=12, level=5),
         PriceUpdate(type='1', action='2', price=9428.50, quantity=600, order_count=35, level=3),
     ], AskTable, [
         PriceUpdate(type='1', action='0', price=9428.00, quantity=40, order_count=2, level=1),
         PriceUpdate(type='1', action='0', price=9429.00, quantity=850, order_count=55, level=3),
         PriceUpdate(type='1', action='0', price=9429.50, quantity=350, order_count=21, level=4),
         PriceUpdate(type='1', action='0', price=9430.00, quantity=150, order_count=12, level=5),
     ]),
    ([
         PriceUpdate(type='0', action='0', price=9428.00, quantity=503, order_count=20, level=1),
         PriceUpdate(type='0', action='0', price=9428.50, quantity=750, order_count=34, level=2),
         PriceUpdate(type='0', action='0', price=9429.00, quantity=400, order_count=25, level=3),
         PriceUpdate(type='0', action='0', price=9429.50, quantity=300, order_count=14, level=4),
         PriceUpdate(type='0', action='0', price=9430.00, quantity=400, order_count=1, level=5),
         PriceUpdate(type='0', action='2', price=9429.50, quantity=300, order_count=25, level=4),
     ], BidTable, [
         PriceUpdate(type='0', action='0', price=9430.00, quantity=400, order_count=1, level=5),
         PriceUpdate(type='0', action='0', price=9429.00, quantity=400, order_count=25, level=3),
         PriceUpdate(type='0', action='0', price=9428.50, quantity=750, order_count=34, level=2),
         PriceUpdate(type='0', action='0', price=9428.00, quantity=503, order_count=20, level=1),
     ])

])
def test_delete(ticks, book_type, result):
    bid_book = book_type(5)

    for price_update in ticks:
        bid_book.update(price_update)

    for i, price in enumerate(bid_book.get_book()):
        assert (result[i] == price)
