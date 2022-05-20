from os import listdir
from os.path import isfile, join





files = [k for k in listdir('db') if 'AUD' in k]

onlyfiles = [f for f in listdir('/db') if isfile(join('/db', f))]