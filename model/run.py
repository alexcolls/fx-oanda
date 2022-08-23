

import json
from datetime import datetime
from src.update_db import update_db
from time import sleep



with open('meta/variables.json') as d:
    variables = json.load(d)
    FIRST_RUN = variables['FIRST_RUN']
    FIRST_YEAR = variables['FIRST_YEAR']



if FIRST_RUN:

    from src.first_run import first_run

    first_run()
    
    sleep(4) # give time to your machine to update FIRST_YEAR meta/variables.json
    


else:
    print('\n> Checking current database...')


"""
 print("This process can take more than 12 hours to complete. So be patient, keep the process running. \n\nMake sure to have a stable internet connection and your laptop pulged in.\n")

    print("\n")

    input('\n<<< Proceed with the above config? press enter to proceed or ctrl-c to exit ')
"""