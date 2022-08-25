

def selectWeek( year, week, filter_order=8, cutoff_freq=0.01  ):

    # plot mids returns
    mids_ = pd.read_csv('db/data/secondary/' + str(year) +'/'+ str(week) +'/'+ 'mids_.csv', index_col=0)
    mids_plt = px.line(mids_, height=800)

    # plot spreads (%%) pips
    spreads_ = pd.read_csv('db/data/primary/' + str(year) +'/'+ str(week) +'/'+ 'spreads.csv', index_col=0)
    spreads_.index = pd.to_datetime(spreads_.index)
    spreads_plt = px.line(spreads_, height=400)

    # plot raw volumes
    volumes_ = pd.read_csv('db/data/primary/' + str(year) +'/'+ str(week) +'/'+ 'volumes.csv', index_col=0)
    volumes_plt = px.line(volumes_, height=400)

    # plot idxs returns
    idxs_ = pd.read_csv('db/data/secondary/' + str(year) +'/'+ str(week) +'/'+ 'idxs_.csv', index_col=0)

    lowpass_, idxs_lp = LowPass( idxs_, filter_order, cutoff_freq  )

    idxs_plt = px.line( idxs_lp, height=800)

    # substract singal noise

    noise_ = idxs_ - lowpass_

    noise_threshold = 0.1

    noise_plt = px.line(noise_, height=600)
    noise_plt.add_hline(y=noise_threshold, line_color='red')
    noise_plt.add_hline(y=-noise_threshold, line_color='green')    

    # trend
    trend_ = pd.DataFrame(index=idxs_.index, columns=idxs_.columns)

    for i in range(2, len(idxs_)):
        for ccy in idxs_.columns:
            trend_[ccy][i] = ( lowpass_[ccy][i] - lowpass_[ccy][i-1] )

    slope_threshold = 0.001

    trend_plt = px.line(trend_, height=600)
    trend_plt.add_hline(y=slope_threshold, line_color='green')
    trend_plt.add_hline(y=-slope_threshold, line_color='red')
    