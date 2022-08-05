
# author: Quantium Rock
# license: MIT

from oanda_api import OandaApi
import sys

if __name__ == "__main__":
   year = int(sys.argv[1])  # input year
   start_week = int(sys.argv[2]) # input start_week
   oanda = OandaApi()
   oanda.storeYearlyQuotes(year, start_week)