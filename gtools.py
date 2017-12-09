import gdax
import sys
import hashlib
import settings
import math

banner = """

                       8I
                       8I
                       8I
                       8I
     ,gggg,gg    ,gggg,8I    ,gggg,gg     ,gg,   ,gg
    dP"  "Y8I   dP"  "Y8I   dP"  "Y8I    d8""8b,dP"
   i8'    ,8I  i8'    ,8I  i8'    ,8I   dP   ,88"
  ,d8,   ,d8I ,d8,   ,d8b,,d8,   ,d8b,,dP  ,dP"Y8,
  P"Y8888P"888P"Y8888P"`Y8P"Y8888P"`Y88"  dP"   "Y88
         ,d8I'
       ,dP'8I       I8                              ,dPYb,
      ,8"  8I       I8                              IP'`Yb
      I8   8I    88888888                           I8  8I
      `8, ,8I       I8                              I8  8'
       `Y8P"        v8      ,ggggg,      ,ggggg,    I8 dP    ,g,
                    I8     dP"  "Y8ggg  dP"  "Y8ggg I8dP    ,8'8,
                   ,I8,   i8'    ,8I   i8'    ,8I   I8P    ,8'  Yb
                  ,d88b, ,d8,   ,d8'  ,d8,   ,d8'  ,d8b,_ ,8'_   8)
                  88P""Y88P"Y8888P"    P"Y8888P"    8P'"Y88P' "YY8P8P

"""

# define our gtools class
class GToolClass:
    accounts = None
    balances = {} # create a dictionary (associative array)
    prices = {}
    client = None

    def __init__(self):
        if settings.use_auth_client:
            self.client = gdax.AuthenticatedClient(settings.api_key, settings.api_secret, settings.api_key_passphrase)
        else:
            self.client = gdax.PublicClient()

    def update_accounts(self):
        if settings.use_auth_client:
            self.accounts = self.client.get_accounts()
            for account in self.accounts:
                if account['currency'] == 'USD':
                    self.balances['USD'] = float(account['balance'])
                if account['currency'] == 'BTC':
                    self.balances['BTC'] = float(account['balance'])
                if account['currency'] == 'ETH':
                    self.balances['ETH'] = float(account['balance'])
                if account['currency'] == 'LTC':
                    self.balances['LTC'] = float(account['balance'])

    def update_prices(self):
        self.prices.clear()
        self.update_price_ltc()
        self.update_price_eth()
        self.update_price_btc()

    def update_price_btc(self):
        btc_price = self.client.get_product_order_book('BTC-USD', level=1)
        self.prices['BTC'] = {} # create nested dicts
        self.prices['BTC']['ask'] = float(btc_price['asks'][0][0])
        self.prices['BTC']['bid'] = float(btc_price['bids'][0][0])

    def update_price_ltc(self):
        ltc_price = self.client.get_product_order_book('LTC-USD', level=1)
        self.prices['LTC'] = {}
        self.prices['LTC']['ask'] = float(ltc_price['asks'][0][0])
        self.prices['LTC']['bid'] = float(ltc_price['bids'][0][0])

    def update_price_eth(self):
        eth_price = self.client.get_product_order_book('ETH-USD', level=1)
        self.prices['ETH'] = {}
        self.prices['ETH']['ask'] = float(eth_price['asks'][0][0])
        self.prices['ETH']['bid'] = float(eth_price['bids'][0][0])


# helper functions

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

def show_prices(gtool):
    print("CURRENT PRICES\n-----------------------------")
    print("Current BTC Bid: $", '{:10,.2f}'.format(gtool.prices['BTC']['bid']))
    print("Current BTC Ask: $", '{:10,.2f}'.format(gtool.prices['BTC']['ask']))
    print("")
    print("Current ETH Bid: $", '{:10,.2f}'.format(gtool.prices['ETH']['bid']))
    print("Current ETH Ask: $", '{:10,.2f}'.format(gtool.prices['ETH']['ask']))
    print("")
    print("Current LTC Bid: $", '{:10,.2f}'.format(gtool.prices['LTC']['bid']))
    print("Current LTC Ask: $", '{:10,.2f}'.format(gtool.prices['LTC']['ask']))
    print("")

def show_balances(gtool):
    total_value = 0
    print("CURRENT BALANCES\n-----------------------------")
    for account in gtool.accounts:
        if account['currency'] == 'USD':
            value = float(account['balance'])
            print ("USD Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print ("USD Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
        if account['currency'] == 'BTC':
            value = float(account['balance']) * gtool.prices['BTC']['ask']
            print ("BTC Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print ("BTC Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
        if account['currency'] == 'ETH':
            value = float(account['balance']) * gtool.prices['ETH']['ask']
            print ("ETH Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print ("ETH Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
        if account['currency'] == 'LTC':
            value = float(account['balance']) * gtool.prices['LTC']['ask']
            print ("LTC Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print ("LTC Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print ("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
    print (        "TOTAL Value $", '{:20,.8f}'.format(total_value))

def main():
    show_banner()
    gtool = GToolClass()
    if settings.use_auth_client:
        gtool.update_accounts()
    gtool.update_prices()
    show_prices(gtool)
    if settings.use_auth_client:
        if "balusd" in sys.argv:
            show_balances(gtool)
        if "btc2usdall" in sys.argv:
            gtool.client.sell(
                # price in USD to sell at
                price=float(gtool.prices['BTC']['ask']),
                # amount of crypto to sell (ALL OF IT)
                size=gtool.balances['BTC'],
                # specifcy market is BTC
                product_id='BTC-USD'
            )
        if "eth2usdall" in sys.argv:
            gtool.client.sell(
                # price in USD to sell at
                price=float(gtool.prices['ETH']['ask']),
                # amount of cyrpto to sell (ALL OF IT)
                size=gtool.balances['ETH'],
                # specifcy market is BTC
                product_id='ETH-USD'
            )
        if "ltc2usdall" in sys.argv:
            gtool.client.sell(
                # price in USD to sell at
                price=float(gtool.prices['LTC']['ask']),
                # amount of crypto to sell (ALL OF IT)
                size=gtool.balances['LTC'],
                # specifcy market is BTC
                product_id='LTC-USD'
            )

def main_old():
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

