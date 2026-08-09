import requests
import pathlib
import json
import re
from pprint import pprint

BASE_URL = "https://api.cer.gov.au/datahub-public/v1"
PARAMS = {}
OUTPUT_DIR = pathlib.Path("data/raw")
TIMEOUT = 60