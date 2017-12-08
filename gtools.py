import gdax
import sys
import hashlib
import settings
import math

# placeholder for relevant data
accounts = None
holdings = {}
prices = None
client = None
btc_price = None
eth_price = None
ltc_price = None

banner = """
                                88
                                88
                                88
           ,adPPYb,d8   ,adPPYb,88  ,adPPYYba,  8b,     ,d8
          a8"    `Y88  a8"    `Y88  ""     `Y8   `Y8, ,8P'
          8b       88  8b       88  ,adPPPPP88     )888(
          "8a,   ,d88  "8a,   ,d88  88,    ,88   ,d8" "8b,
           `"YbbdP"Y8   `"8bbdP"Y8  `"8bbdP"Y8  8P'     `Y8
           aa,    ,88
            "Y8bbdP"

                                                     88
                     ,d                              88
                     88                              88
                   MM88MMM  ,adPPYba,    ,adPPYba,   88  ,adPPYba,
                     88    a8"     "8a  a8"     "8a  88  I8[    ""
                     88    8b       d8  8b       d8  88   `"Y8ba,
                     88,   "8a,   ,a8"  "8a,   ,a8"  88  aa    ]8I
                     "Y888  `"YbbdP"'    `"YbbdP"'   88  `"YbbdP"'

"""


def show_banner():
    print(banner, "\nTool Version    ", file_hash(sys.argv[0]), "\nSettings Version", file_hash('settings.py'), "\n")
    # todo change settings.py argument to use a path relative to this so it works when run from other
    # folders.

def file_hash(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

def show_prices():
    global btc_price, eth_price, ltc_price
    print("Current BTC Bid: $", '{:10,.2f}'.format(float(btc_price['bids'][0][0])))
    print("Current BTC Ask: $", '{:10,.2f}'.format(float(btc_price['asks'][0][0])))
    print("")
    print("Current ETH Bid: $", '{:10,.2f}'.format(float(eth_price['bids'][0][0])))
    print("Current ETH Ask: $", '{:10,.2f}'.format(float(eth_price['asks'][0][0])))
    print("")
    print("Current LTC Bid: $", '{:10,.2f}'.format(float(ltc_price['bids'][0][0])))
    print("Current LTC Ask: $", '{:10,.2f}'.format(float(ltc_price['asks'][0][0])))
    print("")

# list of accounts
def update_accounts():
    global accounts, client, holdings
    accounts = client.get_accounts()
    for account in accounts:
        if account['currency'] == 'USD':
            holdings['USD'] = float(account['balance'])
        if account['currency'] == 'BTC':
            holdings['BTC'] = float(account['balance'])
        if account['currency'] == 'ETH':
            holdings['ETH'] = float(account['balance'])
        if account['currency'] == 'LTC':
            holdings['LTC'] = float(account['balance'])

# get current prices
def update_prices():
    global btc_price, eth_price, ltc_price, client, prices
    btc_price = client.get_product_order_book('BTC-USD', level=1)
    eth_price = client.get_product_order_book('ETH-USD', level=1)
    ltc_price = client.get_product_order_book('LTC-USD', level=1)

def main():
    global btc_price, eth_price, ltc_price, client, accounts, prices, holdings
    show_banner()
    # check to see if we use auth client
    # if started without arguments
    if len(sys.argv) == 1:
        client = gdax.PublicClient()
        update_prices()
        show_prices()
    else:
        if settings.use_auth_client:
            client = gdax.AuthenticatedClient(settings.api_key, settings.api_secret, settings.api_key_passphrase)
            if "balusd" in sys.argv:
                total_value = 0
                update_accounts()
                update_prices()
                show_prices()
                for account in accounts:
                    if account['currency'] == 'USD':
                        value = float(account['balance'])
                        print ("USD Balance: ", '{:20,.8f}'.format(float(account['balance'])))
                        print ("USD Avail:   ", '{:20,.8f}'.format(float(account['available'])))
                        print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
                        total_value += value
                    if account['currency'] == 'BTC':
                        value = float(account['balance']) * float(btc_price['asks'][0][0])
                        print ("BTC Balance: ", '{:20,.8f}'.format(float(account['balance'])))
                        print ("BTC Avail:   ", '{:20,.8f}'.format(float(account['available'])))
                        print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
                        total_value += value
                    if account['currency'] == 'ETH':
                        value = float(account['balance']) * float(eth_price['asks'][0][0])
                        print ("ETH Balance: ", '{:20,.8f}'.format(float(account['balance'])))
                        print ("ETH Avail:   ", '{:20,.8f}'.format(float(account['available'])))
                        print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
                        total_value += value
                    if account['currency'] == 'LTC':
                        value = float(account['balance']) * float(ltc_price['asks'][0][0])
                        print ("LTC Balance: ", '{:20,.8f}'.format(float(account['balance'])))
                        print ("LTC Avail:   ", '{:20,.8f}'.format(float(account['available'])))
                        print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
                        total_value += value
                print (        "TOTAL Value $", '{:20,.8f}'.format(total_value))
            if "btc2usdall" in sys.argv:
                update_accounts()
                update_prices()     # update  prices after account balances so prices are most up to date at time of buy
                client.sell(
                    # prince in USD to sell at
                    price=float(btc_price['asks'][0][0]),
                    # amount of btc to sell (ALL OF IT)
                    size=holdings['BTC'],
                    # specifcy market is BTC
                    product_id='BTC-USD'
                )
            if "usd2btcall" in sys.argv:
                update_accounts()
                update_prices()     # update  prices after account balances so prices are most up to date at time of buy

                money = math.floor(holdings['USD'] * 100.0) / 100.0
                money *= .995
                buy_price = float(btc_price['bids'][0][0])
                buy_size = money/buy_price
                round_factor = 100000000.0
                buy_size = math.floor(buy_size * round_factor) / round_factor
                print("Holdings:" , holdings['USD'])
                print("Money:", money)
                print("Buy Size:", buy_size)
                print("Buy Price:", buy_price)
                print("Cost:", buy_size * buy_price)
                print(client.buy(
                    # USD
                    price=buy_price,
                    # BTC
                    size=buy_size,
                    # specifcy market is BTC
                    product_id='BTC-USD'
                ))
            if "eth2usdall" in sys.argv:
                update_accounts()
                update_prices()     # update  prices after account balances so prices are most up to date at time of buy
                print(client.sell(
                    # prince in USD to sell at
                    price=float(eth_price['asks'][0][0]),
                    # amount of btc to sell (ALL OF IT)
                    size=holdings['ETH'],
                    # specifcy market is BTC
                    product_id='ETH-USD'
                ))
            if "usd2ethall" in sys.argv:
                update_accounts()
                update_prices()     # update  prices after account balances so prices are most up to date at time of buy

                money = math.floor(holdings['USD'] * 100.0) / 100.0
                money *= .995
                buy_price = float(eth_price['bids'][0][0])
                buy_size = money/buy_price
                round_factor = 100000000.0
                buy_size = math.floor(buy_size * round_factor) / round_factor
                print("Holdings:" , holdings['USD'])
                print("Money:", money)
                print("Buy Size:", buy_size)
                print("Buy Price:", buy_price)
                print("Cost:", buy_size * buy_price)
                print(client.buy(
                    # USD
                    price=buy_price,
                    # ETH
                    size=buy_size,
                    # specifcy market is ETH
                    product_id='ETH-USD'
                ))

if __name__ == '__main__':
    main()

