import os
import urllib.request
import zipfile

DATA_DIR = 'data'
WDI_XLSX = os.path.join(DATA_DIR, 'WDIEXCEL.xlsx') # world development indicators
WDI_ZIP = os.path.join(DATA_DIR, 'WDIEXCEL.zip') 
CT_CSV = os.path.join(DATA_DIR, 'CT.csv') # world development indicators

if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(WDI_XLSX):
    zip_path = os.path.join(DATA_DIR, WDI_ZIP)
    print('Downloading WDI dataset...')

    # We go for the Excel doc here because server kept resetting the connection when I tried to download the CSV
    # This reproduced in browser too *shrug*
    urllib.request.urlretrieve('https://databank.worldbank.org/data/download/WDI_excel.zip' , WDI_ZIP)

    print('Unzipping WDI...')
    with zipfile.ZipFile(WDI_ZIP, 'r') as z:
        z.extractall(DATA_DIR)

    os.remove(WDI_ZIP)

if not os.path.exists(os.path.join(DATA_DIR, CT_CSV)):
    print('Download CT data...')
    urllib.request.urlretrieve('https://api.climatetrace.org/emissions_by_subsector_timeseries?interval=year&since=2015&to=2020&download=csv' , CT_CSV)

print('Data successfully downloaded to ./data')