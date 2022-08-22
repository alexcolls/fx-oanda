
# author: Quantium Rock
# license: MIT

from config.keys.oanda_token import TOKEN

AUTH = TOKEN

if len(AUTH) > 0:
    print( '\n', AUTH, '\n' )
    print( '> Key loaded succesfully.', '\n' )
else:
    print( '\nERROR!\n> Insert Oanda credentials TOKEN inside ./config/keys/oanda_token.py')
    print( '> Get yours: https://developer.oanda.com/rest-live-v20/authentication/\n')

# create symbols list

print('\nPortfolio assets:\n')

SYMBOLS = [ 'AUD_CAD', 'AUD_CHF', 'AUD_JPY', 'AUD_NZD', 'AUD_USD', 
            'CAD_CHF', 'CAD_JPY', 'CHF_JPY', 'EUR_AUD', 'EUR_CAD', 
            'EUR_CHF', 'EUR_GBP', 'EUR_JPY', 'EUR_NZD', 'EUR_USD', 
            'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_JPY', 'GBP_NZD', 
            'GBP_USD', 'NZD_CAD', 'NZD_CHF', 'NZD_JPY', 'NZD_USD', 
            'USD_CAD', 'USD_CHF', 'USD_JPY', 'XAG_AUD', 'XAG_CAD',
            'XAG_CHF', 'XAG_EUR', 'XAG_GBP', 'XAG_JPY', 'XAG_NZD',
            'XAG_USD', 'XAU_AUD', 'XAU_CAD', 'XAU_CHF', 'XAU_EUR',
            'XAU_GBP', 'XAU_JPY', 'XAU_NZD', 'XAU_USD', 'XAU_XAG', 
          ]

i = 0
for symbol in SYMBOLS:
    print(symbol)
    i += 1

print('\n>', i, 'assets loaded. Good luck!', '\n')