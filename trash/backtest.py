from os import listdir
import pandas as pd


fee = 0.01  # %

files = [k for k in listdir('db/pairs')]

for file in files:

    sigs = pd.read_csv('db/signals/'+file)
    pair = pd.read_csv('db/pairs/'+file)
    data = pd.merge(sigs, pair, on=['date', 'date'])
    data = data.set_index('date')

    perf = pd.DataFrame(
        columns=['date', 'trend', 'signal', 'trend+signal', 'return'])

    a = 0
    b = 0
    c = 0
    sig = 0
    trend = 0

    for index, row in data.iterrows():

        ret = float(row['return'])

        if trend == 2:
            a = ret-fee
        elif trend == -2:
            a = -ret-fee
        else:
            a = 0

        if sig == 1:
            b = ret-fee
        elif sig == -1:
            b = -ret-fee
        else:
            b = 0

        if trend == 2 and sig == 1:
            c = ret*2-fee*2
        elif trend == -2 and sig == -1:
            c = -ret*2-fee*2
        else:
            c = 0

        perf.loc[len(perf.index)] = [index, a, b, c, ret]

        trend = row['trend']
        sig = row['signal']

    perf = perf.set_index('date')

    perf['trend'] = round(perf['trend'].cumsum(), 2)
    perf['signal'] = round(perf['signal'].cumsum(), 2)
    perf['trend+signal'] = round(perf['trend+signal'].cumsum(), 2)
    perf['return'] = round(perf['return'].cumsum(), 2)

    perf.to_csv('db/backtest/'+file, index=True)

    pd.options.plotting.backend = "plotly"
    plt = perf.plot(x=perf.index, y=perf.columns, title=file[0:7])
    plt.show()

    print(file[0:7])
    input('press enter to continue...')
