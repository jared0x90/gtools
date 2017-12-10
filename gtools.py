#!/usr/bin/env python

""" gtools the even less official gdax python toolbelt """
# python standard libraries
import hashlib
import math
import os
import sys
import argparse

# our settings file
import settings

# "The unofficial Python client for the GDAX API"
# https://github.com/danpaquin/gdax-python
import gdax

BANNER = """

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
            (c) 2017 Jared De Blander. MIT Licensed. See LICENSE.txt

"""

class GToolClass:
    """ a class that handles interacting with gdax """
    accounts = None
    balances = {} # create a dictionary (associative array)
    prices = {}
    client = None

    def __init__(self):
        if settings.USE_AUTH_CLIENT:
            self.client = gdax.AuthenticatedClient(
                settings.API_KEY,
                settings.API_SECRET,
                settings.API_KEY_PASSPHRASE
            )
        else:
            self.client = gdax.PublicClient()

    def update_accounts(self):
        """ retrieve our balances from gdax """
        if settings.USE_AUTH_CLIENT:
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
        """ fetch recent market prices """
        self.prices.clear()
        self.update_price_ltc()
        self.update_price_eth()
        self.update_price_btc()

    def update_price_btc(self):
        """ fetch the price of btc """
        btc_price = self.client.get_product_order_book('BTC-USD', level=1)
        self.prices['BTC'] = {} # create nested dicts
        self.prices['BTC']['ask'] = float(btc_price['asks'][0][0])
        self.prices['BTC']['bid'] = float(btc_price['bids'][0][0])

    def update_price_ltc(self):
        """ fetch the price of ltc """
        ltc_price = self.client.get_product_order_book('LTC-USD', level=1)
        self.prices['LTC'] = {}
        self.prices['LTC']['ask'] = float(ltc_price['asks'][0][0])
        self.prices['LTC']['bid'] = float(ltc_price['bids'][0][0])

    def update_price_eth(self):
        """ fetch the price of eth """
        eth_price = self.client.get_product_order_book('ETH-USD', level=1)
        self.prices['ETH'] = {}
        self.prices['ETH']['ask'] = float(eth_price['asks'][0][0])
        self.prices['ETH']['bid'] = float(eth_price['bids'][0][0])

# helper functions
def show_banner():
    """ print the startup banner """
    print(
        BANNER,
        "\nTool Version    ",
        file_hash(sys.argv[0]),
        "\nSettings Version",
        file_hash(os.path.join(os.path.dirname(__file__), 'settings.py')),
        "\n"
    )

def file_hash(filename):
    """ calculate the sha256 of a file """
    hasher = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as file_in:
        for bytes_in in iter(lambda: file_in.read(128 * 1024), b''):
            hasher.update(bytes_in)
    return hasher.hexdigest()

def show_prices(gtool):
    """ display the most recently observed asks and bids for all currencies """
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
    """ function to display our balances and value in USD """
    total_value = 0
    print("CURRENT BALANCES\n-----------------------------")
    for account in gtool.accounts:
        if account['currency'] == 'USD':
            value = float(account['balance'])
            print("USD Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print("USD Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
        if account['currency'] == 'BTC':
            value = float(account['balance']) * gtool.prices['BTC']['ask']
            print("BTC Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print("BTC Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
        if account['currency'] == 'ETH':
            value = float(account['balance']) * gtool.prices['ETH']['ask']
            print("ETH Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print("ETH Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
        if account['currency'] == 'LTC':
            value = float(account['balance']) * gtool.prices['LTC']['ask']
            print("LTC Balance: ", '{:20,.8f}'.format(float(account['balance'])))
            print("LTC Avail:   ", '{:20,.8f}'.format(float(account['available'])))
            print("Value:      $", '{:20,.8f}'.format(float(value)), "\n")
            total_value += value
    print("TOTAL Value $", '{:20,.8f}'.format(total_value))

def round_usd_down_to_nearest_cent(usd):
    """ round USD amounts down to the nearest cent """
    return round_down_to_nearest_decimal(usd, 2)

def round_down_to_nearest_decimal(value_to_round, digits_of_precision):
    """ round a number down to the specified number of decimal places """
    return (
        math.floor(float(value_to_round) * (10.0 ** digits_of_precision))
        /
        (10.0 ** digits_of_precision)
    )

def new_main():
    """ gtools main function """
    if not settings.HIDE_BANNER:
        show_banner()
    gtool = GToolClass()
    if not settings.USE_AUTH_CLIENT:
        gtool.update_prices()
        show_prices(gtool)
    else:

        # if no arguments dump prices and balances and exit
        if not len(sys.argv) > 1:
            gtool.update_accounts()
            gtool.update_prices()
            show_prices(gtool)
            show_balances(gtool)
            sys.exit(0)

        # Create an argument parser
        parser = argparse.ArgumentParser(
            description='Interact with GDAX via the terminal.'
        )

        # Define arguments
        parser.add_argument(
            "-b", "--balances",
            help="display current balances.",
            action="store_true"
        )

        parser.add_argument(
            "-p", "--prices",
            help="display current prices.",
            action="store_true"
        )

        exchange_group = parser.add_argument_group('exchange')
        exchange_group.add_argument(
            "-e", "--exchange",
            help="currency to source exchange from."
        )

        exchange_group.add_argument(
            "-t", "--to",
            help="currency to trade to."
        )

        exchange_group.add_argument(
            "-a", "--amount",
            help="amount of source currency to use"
        )


        # Parse the arguments
        args = parser.parse_args()

        # this is done after the arg parser to not waste time
        # grabbing data remotely if our args are wrong
        gtool.update_accounts()
        gtool.update_prices()


        # Test the arguments
        if args.prices:
            show_prices(gtool)
        if args.balances:
            show_balances(gtool)


def main():
    """ gtools main function """
    if not settings.HIDE_BANNER:
        show_banner()
    gtool = GToolClass()
    if settings.USE_AUTH_CLIENT:
        gtool.update_accounts()
    gtool.update_prices()
    show_prices(gtool)
    if settings.USE_AUTH_CLIENT:
        # show balances
        if "balusd" in sys.argv:
            show_balances(gtool)

        # convert crypto to usd
        if "btc2usdall" in sys.argv:
            print(gtool.client.sell(
                # price in USD to sell at
                price=float(gtool.prices['BTC']['ask']),
                # amount of crypto to sell (ALL OF IT)
                size=gtool.balances['BTC'],
                # specifcy market is BTC
                product_id='BTC-USD'
            ))
        if "eth2usdall" in sys.argv:
            print(gtool.client.sell(
                # price in USD to sell at
                price=float(gtool.prices['ETH']['ask']),
                # amount of cyrpto to sell (ALL OF IT)
                size=gtool.balances['ETH'],
                # specifcy market is BTC
                product_id='ETH-USD'
            ))
        if "ltc2usdall" in sys.argv:
            print(gtool.client.sell(
                # price in USD to sell at
                price=float(gtool.prices['LTC']['ask']),
                # amount of crypto to sell (ALL OF IT)
                size=gtool.balances['LTC'],
                # specifcy market is BTC
                product_id='LTC-USD'
            ))

        # convert usd to crypto
        if "usd2btcall" in sys.argv:
            # get usd balance to convert to BTC
            money = round_usd_down_to_nearest_cent(gtool.balances['USD'])
            # todo investigate why we cannot place a market order for 100% of USD balance via API
            money *= settings.CASH_TO_CRYPTO_MULTIPLIER

            # calculate buy size
            buy_size = round_down_to_nearest_decimal(
                money / gtool.prices['BTC']['bid'],
                settings.SATOSHI_FACTOR
            )

            # display buy info
            print("USD Balance:", str(gtool.balances['USD']))
            print("Money:", money)
            print("Buy Size:", buy_size)
            print("Buy Price:", gtool.prices['BTC']['bid'])
            print("Cost:", buy_size * gtool.prices['BTC']['bid'])
            print(gtool.client.buy(
                # USD
                price=gtool.prices['BTC']['bid'],
                # BTC
                size=buy_size,
                # specifcy market is BTC
                product_id='BTC-USD'
            ))

        if "usd2ethall" in sys.argv:
            # get usd balance to convert to ETH
            money = round_usd_down_to_nearest_cent(gtool.balances['USD'])
            # todo investigate why we cannot place a market order for 100% of USD balance via API
            money *= settings.CASH_TO_CRYPTO_MULTIPLIER

            # calculate buy size
            buy_size = round_down_to_nearest_decimal(
                money / gtool.prices['ETH']['bid'],
                settings.WEI_FACTOR
            )

            # display buy info
            print("USD Balance:", str(gtool.balances['USD']))
            print("Money:", money)
            print("Buy Size:", buy_size)
            print("Buy Price:", gtool.prices['ETH']['bid'])
            print("Cost:", buy_size * gtool.prices['ETH']['bid'])
            print(gtool.client.buy(
                # USD
                price=gtool.prices['ETH']['bid'],
                # ETH
                size=buy_size,
                # specifcy market is ETH
                product_id='ETH-USD'
            ))

# good ol' boilerplate
if __name__ == '__main__':
    main()
