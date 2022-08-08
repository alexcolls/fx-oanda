
# author: Quantium Rock
# license: MIT

from sys import argv
from asks_bids import AsksBids
from mids import makeMids


if __name__ == "__main__":
	db1 = AsksBids()
	db2 = makeMids()
	if len(argv) > 1:
		if 'check' in argv[1]:
			print(db1.checkDB())
		elif 'update' in argv[1]:
			print(db1.updateDB())
		elif 'mids' in argv[1]:
			print()
		else:
			print('-h for help')
	else:
		print('HELP')
