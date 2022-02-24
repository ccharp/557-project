import os
import urllib.request
import zipfile

from clean import clean

DATA_DIR = "data"
WDI_XLSX = os.path.join(DATA_DIR, "WDIEXCEL.xlsx")  # world development indicators
WDI_ZIP = os.path.join(DATA_DIR, "WDIEXCEL.zip")
CT_CSV = os.path.join(DATA_DIR, "CT.csv")  # world development indicators
NORMALIZED_CO2_DATA = os.path.join(DATA_DIR, "NORMALIZED_CO2_DATA.csv")

if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)


def fetch_data(
    destination_path: str,
    dataset_name: str,
    download_url: str,
    is_zip: bool = False,
    unzipped_path: str = None,
):
    """
    Downloads data from source into DATA_DIR
    Args:
        destination_path:
            Path to download asset from download_url to
        dataset_name:
            Name of dataset (for progress messages)
        download_url:
            URL to get dataset from
        is_zip:
            Optional bool if downloaded asset is a zip file
        unzipped_path:
            Optional string to specify path of unzipped asset.
            Used for checking if we should download the zip asset again.
    """
    if os.path.exists(unzipped_path or destination_path):
        print(f"{dataset_name} dataset exists... skipping download")
    else:
        print(f"Downloading {dataset_name} dataset...")
        # We go for the Excel doc here because server kept resetting the connection when I tried to download the CSV
        # This reproduced in browser too *shrug*
        urllib.request.urlretrieve(download_url, destination_path)

        if is_zip:
            print(f"Unzipping {destination_path}...")
            with zipfile.ZipFile(destination_path, "r") as z:
                z.extractall(DATA_DIR)
            os.remove(destination_path)


# Fetch datasets
fetch_data(
    WDI_ZIP,
    "WDI",
    "https://databank.worldbank.org/data/download/WDI_excel.zip",
    True,
    WDI_XLSX,
)
fetch_data(
    CT_CSV,
    "CT",
    "https://api.climatetrace.org/emissions_by_subsector_timeseries?interval=year&since=2015&to=2020&download=csv",
)
fetch_data(
    NORMALIZED_CO2_DATA,
    "Normalized CO2",
    "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv",
)

print("Data successfully downloaded to ./data")
print("Cleaning data...")
clean(os.path.join(DATA_DIR, "wdi_cleaned.csv"))
print("Cleaned dataset: ./data/wdi_cleaned.csv")
