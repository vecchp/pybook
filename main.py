from pybook import PyBook, HeapBook, SortedDictBook
from pybook.price import cme_price_maker
import random
import time


def get_price_update():
    price_type = random.choice([48, 49])
    action = random.choice([48, 49, 51, 52])
    price = random.uniform(1000.0, 2000.0)
    quantity = random.randint(1, 700)
    order_count = random.randint(1, 20)
    level = random.randint(1, 10)
    return cme_price_maker(None, price_type, action, price, quantity, order_count, level)


def main():
    num_prices = 1000000
    prices = [get_price_update() for _ in range(num_prices)]

    book = PyBook(10, HeapBook)

    start = time.time()
    for price in prices:
        book.update(price)
        #print(book.top_of_book())
    end = time.time()
    total = end - start
    print('{} prices processed in {}s {} pps'.format(num_prices, total, num_prices/total))


if __name__ == '__main__':
    main()
