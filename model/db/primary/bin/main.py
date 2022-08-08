
# author: Quantium Rock
# license: MIT

from data import primaryDB
from sys import argv

if __name__ == "__main__":
	db = primaryDB()
	if len(argv) > 1:
		if 'check' in argv[1]:
			print(db.checkDB())
		elif 'update' in argv[1]:
			print(db.updateDB())
		
		else:
			print('-h for help')
	else:
		print('HELP')
