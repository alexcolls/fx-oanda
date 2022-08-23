

import json
from datetime import datetime
from src.update_db import update_db

with open('meta/variables.json') as d:
    variables = json.load(d)
    FIRST_RUN = variables['FIRST_RUN']


if FIRST_RUN:
    
    from src.first_run import first_run

    first_run()    

else:
    
    ans = input('\nDo you want to update the DB')


