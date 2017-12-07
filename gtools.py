import gdax
import sys
import hashlib
import settings

# declare our public client
client = gdax.PublicClient()

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
          "Y8bbdP"   _              _
                    | |_ ___   ___ | |___
                    | __/ _ \ / _ \| / __|
                    | || (_) | (_) | \__ \\
                     \__\___/ \___/|_|___/
"""


def show_banner():
    print(banner, "\nTool Version    ", file_hash(sys.argv[0]), "\nSettings Version", file_hash('settings.py'), "\n")

def file_hash(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

def show_prices():
    btc_price = client.get_product_order_book('BTC-USD', level=1)
    eth_price = client.get_product_order_book('ETH-USD', level=1)
    ltc_price = client.get_product_order_book('LTC-USD', level=1)
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
            accounts = client.get_accounts()
            if ("balusd" in sys.argv):
                pass

if __name__ == '__main__':
    main()

