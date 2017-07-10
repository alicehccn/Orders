import requests
import json

from collections import defaultdict

__ORDER__ = 'https://gist.githubusercontent.com/ericve25/4058b6625fc0976700b88bd0135eb060/raw/1111162140de8962ed2fd89a71094e92573eeaff/orders.json'
__FEE__ = 'https://gist.githubusercontent.com/ericve25/4058b6625fc0976700b88bd0135eb060/raw/1111162140de8962ed2fd89a71094e92573eeaff/fees.json'


def print_header(header):
    print '=' * 60
    print header
    print '=' * 60


def price_to_int(s):
    return int(s.replace('.00', ''))


def price_to_str(i):
    return '$%s%s' % (str(i), '.00')


def request_get(url):
    response = requests.get(url)
    return json.loads(response.content)


def get_fees(url):
    rows = request_get(__FEE__)
    dct = {row['order_item_type']: row for row in rows}
    return dct


def print_json(dict_list, filename):
    with open(filename, 'w') as outfile:
        json.dump(dict_list, outfile, indent=4, separators=(',', ': '))
        print 'Output written to %s' % filename


def main():
    fees = get_fees(__FEE__)
    orders = request_get(__ORDER__)
    # Challenge 1
    print_header('Challenge 1: Fees')
    order_json = []
    distribution_json = []
    for order in orders:
        print 'Order ID: %s' % order['order_number']
        total = 0
        dct = defaultdict(list)
        dct['order_id'] = order['order_number']
        for item in order['order_items']:
            types = {row['type']: row['amount'] for row in fees[item['type']]['fees']}
            price = price_to_int(types['flat'])
            if item['pages'] > 1:
                price += price_to_int(types['per-page']) * (item['pages']-1)
            total += price
            price = price_to_str(price)
            print '    Order item %s: %s' % (item['type'], price)
            # Prep json object
            order_item = {}
            order_item['order_type'] = item['type']
            order_item['price'] = price
            dct['order_item'].append(order_item)
        dct['total'] = total
        order_json.append(dct)
        print '    Order total: %s' % total
        print '\n'

    # Challenge 2
    print_header('Challenge 2: Distributions')
    for order in orders:
        print 'Order ID: %s' % order['order_number']
        for item in order['order_items']:
            types = {row['type']: row['amount'] for row in fees[item['type']]['fees']}
            total = price_to_int(types['flat'])
            dct = defaultdict(list)
            dct['order_id'] = order['order_number']
            dct['Fund'] = {}
            for d in fees[item['type']]['distributions']:
                total -= (price_to_int(d['amount']))
                dct['Fund'][d['name']] = d['amount']
                print '    Fund - %s: $%s' % (d['name'], d['amount'])
            if total > 0:
                print '    Fund - Other: %s' % price_to_str(total)
            distribution_json.append(dct)
            print '\n'

    # Challenge 3
    print_header('Challenge 3: API')
    print_json(order_json, 'api_1.json')
    print_json(distribution_json, 'api_2.json')
    print '\n'
    print '=' * 60
    print 'Done.'


if __name__ == '__main__':
    main()
