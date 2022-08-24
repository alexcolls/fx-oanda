# cot_downloader.py

# Download all available CoT FuturesOnly reports from CFTC website

import os
import requests

from bs4 import BeautifulSoup
from pathlib import Path
from zipfile import ZipFile


def cot_bulk_downloader():
    """ Downloads all standard Commitment of Traders Futures only reports. """
    url = 'https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm'
    out_path = Path.cwd() / 'data-sets' / 'commitments-of-traders'
    if out_path.exists():  # avoid re-downloading the script if the files have already been downloaded
        return 0
    os.makedirs(out_path, exist_ok=True)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for name in soup.findAll('a', href=True):
        file_url = name['href']
        if file_url.endswith('.zip'):
            filename = file_url.split('/')[-1]
            if 'deacot' in filename:
                out_name = out_path.joinpath(filename)
                zip_url = 'https://www.cftc.gov/files/dea/history/' + filename
                req = requests.get(zip_url, stream=True)
                if req.status_code == requests.codes.ok:
                    if filename.__contains__('2003'):
                        break
                    print(f'Downloading {filename} . . .')
                    with open(out_name, 'wb') as f:
                        for chunk in req.iter_content():
                            if chunk:  # ignore keep-alive requests (?)
                                f.write(chunk)
                        f.close()

    print('Finished downloading reports')
    return 0

def bulk_unzipper(directory):
    """ Unzips all archives within the CoT directory. """
    for file in directory.iterdir():
        if str(file).endswith('.zip'):
            print(f'Unzipping {file} . . .')
            with ZipFile(file, 'r') as zip_object:
                filename = zip_object.filename.split('/')[-1]  # after split consider only the 'deacotXXXX.zip part
                filename = filename.split('.zip')[0]           # consider only the 'deacotXXXX' string
                zip_object.extractall(directory / filename)
    return 0

if __name__ == '__main__':
    try:
        return_val = cot_bulk_downloader()
        if return_val == 0:  # hunky-dory so proceed to unzip
            cot_dir = Path.cwd() / 'cots_raw'  # path created by bulk downloader so no I/O error 
            bulk_unzipper(cot_dir)
    except Exception as exception:
        print(f'Unexpected error: {exception}')