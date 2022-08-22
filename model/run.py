

import os
import json


with open('model/meta/variables.json', 'r') as f:
   data = json.load(f)

print(data)

f = open('model/meta/variables.txt', 'r')
print(json(f))


if FIRST_RUN:

    print("\n> Hi! This is your first run! Welcome! \n\nLet's check your local python configuration. \n\n< Press enter to proceed.")

    # confirm
    input()
    try:
        os.system("python --version")
        print('installed.\n')

        os.system("pip3 --version")
        os.system("pip install --upgrade pip")

        
        os.system("\npip install requirements.txt ")
    except:
        print("\n> Please, install latest Python3 in your system: https://www.python.org/downloads/")


    print("\n\n> Your local database is empty. You need to download multiple datasets in order to run this model. \n\n> It take time to download and process 17 years of 1 minute data-points for multiple assets.")
    print("\n> How do you wanna proceed?", "\n  a : Download only last 3 years of data. (1-2 hours) \n  b : Download full history from 2005 (6-12 hours)")
    input(" insert a or b and press enter \n >>> ")
    print("so make sure to have a stable internet connection and your laptop pulged in.\n")

    print("\n")

    import config.config

    input('\n<<< Proceed with the above config? press enter to proceed or ctrl-c to exit ')
else:
    print('\n> Checking current database...')