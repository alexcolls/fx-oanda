
import json
from datetime import datetime


from db.bin.primary import PrimaryData

def update_db():

    primaryData = PrimaryData()

    primaryData.checkDB()

    input("\nUpdate primary database?\n> Press Enter to proceed\n\n>>> ")

    # update DB
    start_time = datetime.utcnow()
    print('\nUpdating database... starting UTC time: ', start_time)
    primaryData.updateDB()

    final_time = datetime.utcnow()
    print(start_time, final_time)
    primaryData.checkDB()