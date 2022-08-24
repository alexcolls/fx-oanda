
import os
import json
from db.bin.update_db import updateDB
from src.plot_week import plotWeek


with open('meta/variables.json') as d:
    variables = json.load(d)
    FIRST_RUN = variables['FIRST_RUN']


if FIRST_RUN:

    from src.first_run import firstRun
    firstRun()    

else:

    updateDB()

    ans = input('\n> Do you want to open the model dashboard \n\n >>> Press Enter \n ')

    os.system("python src/_dash.py")




    




