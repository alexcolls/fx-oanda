
import os
import json
from datetime import datetime

def first_run():

    print("\n> Hi! This is your first run! Welcome! \n\nLet's check your local python configuration.")
    # confirm
    input("\n\n> Press Enter to proceed or Ctrl-C to exit \n\n>>> ")

    try:
        print('\n')
        os.system("python --version")
        print('installed.\n')

        ans = input('\nDo you want to install/update program dependencies? \n\n(y) yes or (n) no \n\n >>> ')
        if ans.__contains__('y'):
            print('\nupdating pip...\n')
            os.system("pip3 --version")
            os.system("pip3 install --upgrade pip")
            print('\ninstalling requiered dependencies...\n')
            os.system("pip3 install requirements.txt ")
    except:
        print("\nPlease, install latest Python3 in your system: https://www.python.org/downloads/")

    print('\n# \n\n## \n\n\n###')

    print("\n\n> Your local database is empty. You need to download multiple datasets in order to run this model. \nIt take time to download and process 17 years of 1 minute data-points for multiple assets.")

    print("""
> How do you wanna proceed?

    a : Download only last 3 years of data (1-2 hours) 
    b : Download last 10 years of data (6-12 hours) 
    c : Download full history since 2005 (12-24 hours)""")
    
    ans = input("\n > Insert (a) or (b) or (c) and press Enter \n\n >>> ")

    with open("meta/variables.json") as x:
        variables = json.load(x)

    if ans.__contains__('a'):
        variables['FIRST_YEAR'] = datetime.utcnow().year - 3

    elif ans.__contains__('b'):
        variables['FIRST_YEAR'] = datetime.utcnow().year - 10

    elif ans.__contains__('c'):
        variables['FIRST_YEAR'] = 2005

    with open("meta/variables.json", "w") as x:
        json.dump(variables, x)

    print(f"\nDatabase starting year {variables['FIRST_YEAR']}...\n")