
# Oanda parameters
GRANULARITY = 'D'  # Candlesticks period. I.e. H1, H4, H8, D
# Number of last candle to request. Also, period for the Lowwpass filter.
LOOKBACK = 30

# Lowpass filter parameters
N = 2  # filter order
Wn = 0.3  # cutoff frequency

# Instruments
symbols = [
    'AUD_CAD', 'AUD_CHF', 'AUD_HKD', 'AUD_JPY', 'AUD_NZD', 'AUD_SGD', 'AUD_USD', 'CAD_CHF', 'CAD_HKD', 'CAD_JPY', 'CAD_SGD', 'CHF_HKD', 'CHF_JPY', 'EUR_AUD',      'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_HKD', 'EUR_JPY', 'EUR_NZD', 'EUR_SGD', 'EUR_USD', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_HKD', 'GBP_JPY', 'GBP_NZD', 'GBP_SGD', 'GBP_USD', 'HKD_JPY', 'NZD_CAD', 'NZD_CHF', 'NZD_HKD', 'NZD_JPY', 'NZD_SGD', 'NZD_USD', 'SGD_CHF', 'SGD_HKD', 'SGD_JPY', 'USD_CAD', 'USD_CHF', 'USD_HKD', 'USD_JPY', 'USD_SGD']

# Currencies
indexes = ['AUD', 'CAD', 'CHF', 'EUR',
           'GBP', 'HKD', 'JPY', 'NZD', 'SGD', 'USD']
