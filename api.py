import requests
import json

__ORDER__ = 'https://gist.githubusercontent.com/ericve25/4058b6625fc0976700b88bd0135eb060/raw/1111162140de8962ed2fd89a71094e92573eeaff/orders.json'
__FEE__ = 'https://gist.githubusercontent.com/ericve25/4058b6625fc0976700b88bd0135eb060/raw/1111162140de8962ed2fd89a71094e92573eeaff/fees.json'


def request_get(url):
    response = requests.get(url)
    return json.loads(response.content)


def main():
    fees = request_get(__FEE__)
    orders = request_get(__ORDER__)

    import pdb; pdb.set_trace()


if __name__ == '__main__':
    main()
