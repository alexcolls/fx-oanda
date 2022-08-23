
import json
from datetime import datetime
from db.bin.primary import PrimaryData


def update_db():

    with open("meta/variables.json") as x:
        FIRST_YEAR = json.load(x)['FIRST_YEAR']

    primaryData = PrimaryData( start_year=FIRST_YEAR )

    # user confirmation
    input('\nUpdate primary database?\n> Press Enter to proceed\n\n>>> ')

    # update DB    
    primaryData.updateDB()

    

