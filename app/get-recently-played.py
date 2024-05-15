from utils.authentication import Authenticator
from datetime import datetime
import requests
import json
from urllib.parse import urlencode

import logging
from datetime import datetime

logging.basicConfig(
    filename=f"log/fetch-{datetime.now().strftime('%Y-%m-%d')}.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

auth = Authenticator("env.conf")
is_near_expire = auth.is_token_near_expires_in_15_min()

if __name__ == "__main__":
    if is_near_expire:
        logging.info("REQUEST: Refresh Token")
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
    API_URI = (
        f"https://api.spotify.com/v1/me/player/recently-played?{urlencode(path_params)}"
    )

    logging.info(f'GET: URL("{API_URI}")')
    response = requests.get(API_URI, headers=headers, timeout=10).json()

    file_name = f"landing/{int(datetime.now().timestamp())}_spotify_recent_50.json"
    with open(file_name, "w") as tempfile:
        json.dump(response, indent=2, fp=tempfile)
