

import json
from src.update_db import updateDB
from src.plot_week import plotWeek


with open('meta/variables.json') as d:
    variables = json.load(d)
    FIRST_RUN = variables['FIRST_RUN']


if FIRST_RUN:

    from src.first_run import firstRun
    firstRun()    

else:

    updateDB()

    ans = input('\nDo you want to plot last week? \n\n>>> ')

    plotWeek(2022,32)



    




