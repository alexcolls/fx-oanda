
FX G10 Trading Index Model with Oanda Broker

How to use:

1. Run in the project directory the following commands:

```console
>>> python db.py [granularity] [periods]
```

Example:
```console
python db.py D 3000
```
```console
python db.py H1 200 
```

- It will update the db/pairs and will create the currency indexes.
- Note that Oanda does not provide history below 5000 candles. So max period is 5k.

2. After db is succesfully updated, run:
```console
python signals.py 
```

- You can play with the parameters lowpass filter -> filter order & cutoff frequency

3. With the signals created in db/signals, now let's backtest it:
```console
python backtest.py
```

- For performance reasons each currency pair is backtested after pressing enter. Follow the console instructions. 
- You can play with the fee parameter in the script.



In the folder you have some scripts I made during the strategy development process. Only for testing purpose.

In the folder bin you have the trading system ready to deploy. Just modify the parameters in the params.py file.

WARNING: If you are trading in a real account make sure you know what you are doing. All gains or losses caused by the system will be under your responsability.
