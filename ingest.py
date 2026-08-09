import requests
import pathlib
import json
import re
from pprint import pprint

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

nger = make_api_call(
    url = f'{BASE_URL}/api/Schemes/NGER/DatasetCatalogItems',
    printout=False
)

# for item in nger:
#     for key, value in item.items():
#         if isinstance(value, str) and "designated generation facility" in value:
#             print(f'{key}\n{value}\n') 

generation = [item for item in nger if item["displayName"].startswith(STEM)]

# testing each id and name pulled correctly
# print("Found:", len(generation))

for item in generation:
    id = item["id"]
    year = re.search(r"(\d{4})[-–](\d{2})", item["displayName"])
    year = f'{year.group(1)[2:]}{year.group(2)}'
    make_api_call(
        url = f'{BASE_URL}/api/Dataset/NGER/dataset/{id}/download'
    )

