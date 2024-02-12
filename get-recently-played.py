from utils.authentication import Authenticator
from datetime import datetime
import requests
import json
from urllib.parse import urlparse, urlencode

auth = Authenticator("env.conf")
is_near_expire = auth.is_token_near_expires_in_15_min()

if (not is_near_expire):
    # CLIENT_KEY_B64: str = auth.get_client_key_base64()
    access_token = auth.get_access_token()
    if access_token['state'] == 0:
        headers: dict = {
            "Authorization": f"Bearer {access_token['access_token']}"
        }
        path_params = {
            "limit": 3,
            # "after": ,# Unix timestamp in millisecond
            "before": 1707674764098,# Unix timestamp in millisecond
        }
        API_URL = f"https://api.spotify.com/v1/me/player/recently-played?{urlencode(path_params)}"
        response = requests.get(API_URL, headers=headers, timeout=10)
        response = response.json()
        with open("temp_result.json", 'w') as tempfile:
            json.dump(response, indent=2, fp=tempfile)
        print(json.dumps(response, indent=2))
    elif access_token['state'] == 1:
        print("Access token error")
