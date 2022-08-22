
# model main configuratrion

# a) select trading universe:

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


# b) model granularity (S5, M1, M15, H1, H8, D)

TIMEFRAME = 'M1'