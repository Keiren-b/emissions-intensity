import requests
import pathlib
import json
import re
from pprint import pprint
import pandas as pd

#----------------------------------------------------------------------------------------
# format for downloading CER data through API:
# /api/Dataset/{schemeId}/dataset/{datasetId}/download
# Params: schemeId (req), datasetId (req), format, entitlement
#----------------------------------------------------------------------------------------
# NGER dataset

BASE_URL = "https://api.cer.gov.au/datahub-public/v1"
PARAMS = {}
OUTPUT_DIR = pathlib.Path("data/raw")
TIMEOUT = 60
STEM = "Greenhouse and energy information by designated generation facility"


def make_api_call(url, 
                  method="get", 
                  data=None, 
                  params=None, 
                  headers=None, 
                  timeout = TIMEOUT,
                  printout = True):
    request_method = getattr(requests, method.lower())
    try:
        response = request_method(
            url,
            json=data,
            params=params,
            headers=headers,
            timeout = TIMEOUT
        )
        response.raise_for_status()
        if 'application/json' in response.headers.get('content-type', ''):
            if printout == True:
                print("STATUS:", response.status_code)
                print("TYPE:", response.headers.get("content-type"))
                print("FIRST BIT:", response.text[:300])
            return response.json()
        else:
            if printout == True:
                print("STATUS:", response.status_code)
                print("TYPE:", response.headers.get("content-type"))
                print("FIRST BIT:", response.text[:300])
            return response.text
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        try:
            error_details = response.json()
            print(f"Error details: {error_details}")
        except:
            print(f"Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Connection Error: Failed to connect to the API")
        
    except requests.exceptions.Timeout:
        print("Timeout Error: The request timed out")
        
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        
    return None

# Get names of Datasets
nger = make_api_call(
    url = f'{BASE_URL}/api/Schemes/NGER/DatasetCatalogItems',
    printout=False
)

# Create list of dataset names
generation = [item for item in nger if item["displayName"].startswith(STEM)]

def download_data(filenames: List )
for item in generation:
    dataset_id = item["id"]

    match = re.search(r"(\d{4})[-–](\d{2})", item["displayName"])
    year = f"{match.group(1)}-{match.group(2)}"

    rows = make_api_call(
        url=f"{BASE_URL}/api/ODataDataset/NGER/dataset/{dataset_id}",
        printout=False
    )

    if not rows:
        print(f"FAILED: {dataset_id} {year}")
        continue

    for row in rows:
        row["financial_year"] = year

    df = pd.DataFrame(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_DIR / f"nger_generation_{year}.parquet", index=False)
    if year in ["2012-13", "2020-21"]:
        print(df.head(5))
    print(f"{year}: {len(rows)} rows, {len(df.columns)} columns")
    print(f'{df.columns}\n')
