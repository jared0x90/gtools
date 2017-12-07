import gdax
import sys
import hashlib
import settings

# declare our public client
client = gdax.PublicClient()

# get current prices
btc_price = client.get_product_order_book('BTC-USD', level=1)
eth_price = client.get_product_order_book('ETH-USD', level=1)
ltc_price = client.get_product_order_book('LTC-USD', level=1)

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
    print("Current BTC Bid: $", '{:10,.2f}'.format(float(btc_price['bids'][0][0])))
    print("Current BTC Ask: $", '{:10,.2f}'.format(float(btc_price['asks'][0][0])))
    print("")
    print("Current ETH Bid: $", '{:10,.2f}'.format(float(eth_price['bids'][0][0])))
    print("Current ETH Ask: $", '{:10,.2f}'.format(float(eth_price['asks'][0][0])))
    print("")
    print("Current LTC Bid: $", '{:10,.2f}'.format(float(ltc_price['bids'][0][0])))
    print("Current LTC Ask: $", '{:10,.2f}'.format(float(ltc_price['asks'][0][0])))
    print("")

def main():
    show_banner()
    show_prices()
    # check to see if we use auth client
    # if started without arguments
    if len(sys.argv) > 1:
        if settings.use_auth_client:
            client = gdax.AuthenticatedClient(settings.api_key, settings.api_secret, settings.api_key_passphrase)
            if ("balusd" in sys.argv):
                total_value = 0.0
                accounts = client.get_accounts()
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

            print (            "TOTAL Value $", '{:20,.8f}'.format(total_value))


if __name__ == '__main__':
    main()

