import os
import urllib.request
import zipfile

DATA_DIR = "data"
WDI_XLSX = os.path.join(DATA_DIR, "WDIEXCEL.xlsx")  # world development indicators
WDI_ZIP = os.path.join(DATA_DIR, "WDIEXCEL.zip")
CT_CSV = os.path.join(DATA_DIR, "CT.csv")  # world development indicators
NORMALIZED_CO2_DATA = os.path.join(DATA_DIR, "NORMALIZED_CO2_DATA.csv")
ANNUAL_MEAN_CO2 = os.path.join(DATA_DIR, "ANNUAL_MEAN_CO2.csv")
ANNUAL_MEAN_GROWTH_CO2 = os.path.join(DATA_DIR, "ANNUAL_MEAN_GROWTH_CO2.csv")
ANNUAL_MEAN_CH4 = os.path.join(DATA_DIR, "ANNUAL_MEAN_CH4.txt")
ANNUAL_MEAN_GROWTH_CH4 = os.path.join(DATA_DIR, "ANNUAL_MEAN_GROWTH_CH4.txt")
ANNUAL_MEAN_N2O = os.path.join(DATA_DIR, "ANNUAL_MEAN_N2O.txt")
ANNUAL_MEAN_GROWTH_N2O = os.path.join(DATA_DIR, "ANNUAL_MEAN_GROWTH_N2O.txt")
ANNUAL_MEAN_SF6 = os.path.join(DATA_DIR, "ANNUAL_MEAN_SF6.txt")
ANNUAL_MEAN_GROWTH_SF6 = os.path.join(DATA_DIR, "ANNUAL_MEAN_GROWTH_SF6.txt")

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
        print("Done!")


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

fetch_data(
    ANNUAL_MEAN_CO2,
    "Annual marine surface CO2",
    "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv",
)
fetch_data(
    ANNUAL_MEAN_GROWTH_CO2,
    "Annual marine surface CO2 growth",
    "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_gr_gl.csv",
)
fetch_data(
    ANNUAL_MEAN_CH4,
    "Annual marine surface CH4",
    "https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.txt",
)
fetch_data(
    ANNUAL_MEAN_GROWTH_CH4,
    "Annual marine surface CH4 growth",
    "https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_gr_gl.txt",
)
fetch_data(
    ANNUAL_MEAN_N2O,
    "Annual marine surface N2O",
    "https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_annmean_gl.txt",
)
fetch_data(
    ANNUAL_MEAN_GROWTH_N2O,
    "Annual marine surface N2O growth",
    "https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_gr_gl.txt",
)
fetch_data(
    ANNUAL_MEAN_SF6,
    "Annual marine surface SF6",
    "https://gml.noaa.gov/webdata/ccgg/trends/sf6/sf6_annmean_gl.txt",
)
fetch_data(
    ANNUAL_MEAN_GROWTH_SF6,
    "Annual marine surface SF6 growth",
    "https://gml.noaa.gov/webdata/ccgg/trends/sf6/sf6_gr_gl.txt",
)

print("Data successfully downloaded to ./data")
