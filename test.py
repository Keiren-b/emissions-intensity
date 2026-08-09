import requests
import pathlib
import json
import re
from pprint import pprint

BASE_URL = "https://api.cer.gov.au/datahub-public/v1"
PARAMS = {}
OUTPUT_DIR = pathlib.Path("data/raw")
TIMEOUT = 60
STEM = "Greenhouse and energy information by designated generation facility"

# https://data.cer.gov.au/datasets/NGER/ID0082

# baseUrl/api/Schemes

def make_api_call(url, method="get", data=None, params=None, headers=None, timeout = TIMEOUT):

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
            print("STATUS:", response.status_code)
            print("TYPE:", response.headers.get("content-type"))
            print("FIRST BIT:", response.text[:300])
            return response.json()
        else:
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

schemes = make_api_call(
    url = f'{BASE_URL}/api/Schemes'
)

for scheme in schemes:
    print(f'{scheme["displayName"]} : {scheme["id"]}')

# nger = make_api_call(
#     url = f'{BASE_URL}/api/Schemes/NGER/DatasetCatalogItems'
# )

# for item in nger:
#     for key, value in item.items():
#         if isinstance(value, str) and "designated generation facility" in value:
#             print(f'{key}\n{value}\n') 


# generation = [item for item in nger if item["displayName"].startswith(STEM)]
# print(generation)
# print("Found:", len(generation))
# for item in generation:
#     print(item["id"], item["displayName"])

# def extract_year(display_name):
#     """Find a financial year like 2021-22 or 2023–24 in the name."""
#     match = re.search(r"(\d{4})[-–](\d{2})", display_name)
#     if match is None:
#         return None
#     return f"{match.group(1)}-{match.group(2)}"

# years = []
# for item in generation:
#     year = extract_year(item["displayName"])
#     years.append({"id": item["id"], "year": year})
#     # print(item["id"], "->", extract_year(item["displayName"]))
# # years.sort(key=lambda x: x["id"])

# print(years)