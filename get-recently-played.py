from utils.authentication import Authenticator
from datetime import datetime
import requests
import json
from urllib.parse import urlencode

auth = Authenticator("env.conf")
is_near_expire = auth.is_token_near_expires_in_15_min()

if __name__ == "__main__":
    if is_near_expire:
        auth.refresh_access_token()
    access_token = auth.get_access_token()

    if access_token["state"] != 0:
        raise Exception("Access token error")

    headers: dict = {"Authorization": f"Bearer {access_token['access_token']}"}
    path_params = {
        "limit": 50,
        # Current Unix timestamp in millisecond
        "before": int(datetime.timestamp(datetime.now()) * 1000),
        # Unix timestamp in millisecond
        # "after": ,
    }
    API_URL = (
        f"https://api.spotify.com/v1/me/player/recently-played?{urlencode(path_params)}"
    )
    response = requests.get(API_URL, headers=headers, timeout=10).json()

    file_name = f"landing/{int(datetime.now().timestamp())}_spotify_recent_50.json"
    with open(file_name, "w") as tempfile:
        json.dump(response, indent=2, fp=tempfile)
