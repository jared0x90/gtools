""" where all gtools settings are stored """

###############################################################################
############ general settings and constants
###############################################################################
# show/hide the ascii art banner
HIDE_BANNER = False
# 0.00000001 smallest unit of BTC
SATOSHI_FACTOR = 8
# 0.000000000000000001 smallest unit of ethereum
WEI_FACTOR = 18

###############################################################################
############ api settings
###############################################################################
USE_AUTH_CLIENT = False
API_KEY_PASSPHRASE = ""
API_SECRET = ""
API_KEY = ""

###############################################################################
############ trading settings
###############################################################################
#
# for some reason the API won't let us place a cash to crypto market buy with
# full amounts. gives insufficient funds errors. perhaps it's an issue with
# the gdax api wrapper that is used.
CASH_TO_CRYPTO_MULTIPLIER = 0.995
