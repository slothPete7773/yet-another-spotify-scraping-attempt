from urllib.parse import urlencode
import base64
import datetime
import requests
from typing import Dict

from configparser import ConfigParser
config = ConfigParser()


def write_config(config_filepath: str, section_name: str, config_info: Dict, config_parser: ConfigParser): 
            for key in config_info.keys():
                config_parser.set(section_name, key, config_info[key])
            with open(config_filepath, 'w') as config_file:
                config_parser.write(config_file)
        

class Authenticator():

    def __init__(self, config_file) -> None:
        config.read(config_file)

        client_id = config.get("spotify_credential", "client_id")
        client_secret = config.get("spotify_credential", "client_secret")
        redirect_uri = config.get("spotify_credential", "redirect_uri")
        

        self.__client_id = client_id
        self.__client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "user-top-read user-read-currently-playing user-read-recently-played user-read-private user-read-email"
        self.state = "hello42"
        self.show_dialog = ""
        self.auth_code = ""
        self.tokens = {}
        self.config = config
        self.config_file = config_file

        self.OAUTH_ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
        self.API_v1_URL = "https://api.spotify.com/v1"


    def get_authorization_url(self) -> str: 
        params = {
            "response_type": "code",
            "client_id": self.__client_id,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "state": "state"
        }
        return f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    
    def get_client_key_base64(self) -> str: 
        return base64.b64encode(f"{self.__client_id}:{self.__client_secret}".encode()).decode()

    def get_access_token(self) -> str: 
        is_authorize: str = self.config.get("token_info", "authorize?")

        if (is_authorize.lower() == "true"):
            return {
                "state": 0,
                "access_token": self.config.get("token_info", "access_token")
            }
        else:
             return {
                "state": 1,
                "access_token": None
             }
        

    def refresh_access_token(self) -> dict:
        is_authorize: str = self.config.get("token_info", "authorize?")
        if (is_authorize.lower() == "false"):
            raise PermissionError
        
        payload: dict = {
            "grant_type": "refresh_token",
            "refresh_token": f'{self.config.get("token_info", "refresh_token")}'
        }

        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(self.get_client_key_base64())
        }
        r = requests.post(self.OAUTH_ACCESS_TOKEN_URL, headers=headers, data=payload)
        token_info = r.json()

        new_expire_dt = datetime.datetime.now() + datetime.timedelta(seconds=token_info['expires_in'])
        new_expire_stamp = new_expire_dt.timestamp()
        
        data = {
            "expires_at": str(new_expire_stamp),
            "access_token": token_info["access_token"],
        }
        write_config(self.config_file, "token_info", data, self.config)
        token_info['expires_at'] = new_expire_stamp
        return {
             "token_info": token_info,
             "state": 0
        }
    
    def is_token_near_expires_in_15_min(self):
        _expire_timestamp = self.config.get("token_info", "expires_at")
        expire_timestamp = datetime.datetime.fromtimestamp(float(_expire_timestamp))
        target_time = expire_timestamp - datetime.timedelta(minutes=15)
        # print(expire_timestamp)
        return  target_time < datetime.datetime.now()