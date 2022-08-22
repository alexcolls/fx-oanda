
import os
import json
from datetime import datetime


from db.bin.primary import PrimaryData


with open('meta/variables.json') as d:
    variables = json.load(d)
    FIRST_RUN = variables['FIRST_RUN']
    FIRST_YEAR = variables['FIRST_YEAR']

primaryData = PrimaryData()

if FIRST_RUN:

    from src.first_run import first_run

    first_run()
    
    primaryData.checkDB()

    input("\nUpdate database?\n> Press Enter to proceed\n\n>>> ")

    # update DB
    start_time = datetime.utcnow()
    print('\nUpdating database... starting UTC time: ', start_time)
    primaryData.updateDB()

    final_time = datetime.utcnow()
    print(start_time, final_time)
    primaryData.checkDB()
   
else:
    print('\n> Checking current database...')
    primaryData.checkDB()
    primaryData.updateDB()

"""
 print("This process can take more than 12 hours to complete. So be patient, keep the process running. \n\nMake sure to have a stable internet connection and your laptop pulged in.\n")

    print("\n")

    input('\n<<< Proceed with the above config? press enter to proceed or ctrl-c to exit ')
"""