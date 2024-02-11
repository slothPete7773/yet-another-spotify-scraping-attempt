# from pathlib import Path
import time
from urllib.parse import urlparse, urlencode
from typing import Dict, Type, Optional
from dataclasses import dataclass
import base64
import datetime
import requests

# import spotipy
# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyOAuth
# from spotipy.exceptions import 


# import configparser
from configparser import ConfigParser
config = ConfigParser()

# from pydantic import BaseModel

class UnixMilliSecond:
    def __init__(self) -> None:
        self.__timestamp: int = None

    def get_current_Unix_milliseconds_timestamp(self) -> int:
        now_ms = int( time.time_ns() / 1000 )

        print( now_ms )

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

    
    def get_access_token(self, code: str = None) -> str: 
        is_authorize: str = self.config.get("token_info", "authorize?")
        prev_scope = set(self.config.get("token_info", "scope").split(" "))
        curr_scope = set(self.scope.split(" "))

        if ((is_authorize.lower() == "true") and (curr_scope == prev_scope)):
            print("already true, give access_token")
            return self.config.get("token_info", "access_token")
        
        CLIENT_KEY_B64: str = self.get_client_key_base64() # base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(CLIENT_KEY_B64)
        }
        payload: dict = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        
        OAUTH_ACCESS_TOKEN_URL: str = self.OAUTH_ACCESS_TOKEN_URL
        r = requests.post(OAUTH_ACCESS_TOKEN_URL, headers=headers, data=payload)
        token_info = r.json()
        print(f"Token Info: \n{token_info}")

        
        token_info_dict = {
            "access_token": token_info["access_token"],
            "token_type": token_info["token_type"],
            "expires_in": str(token_info["expires_in"]),
            "scope": token_info["scope"],
            "expires_at": str((datetime.datetime.now() + datetime.timedelta(seconds=token_info["expires_in"])).timestamp()),
            "refresh_token": token_info["refresh_token"],
            "authorize?": "true",
        }
        write_config(self.config_file, "token_info", token_info_dict, self.config)
        return token_info["access_token"]

    def refresh_access_token(self) -> dict:
        print("Hello")
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

        print(f"Time now: {datetime.datetime.now()}")
        new_expire_dt = datetime.datetime.now() + datetime.timedelta(seconds=token_info['expires_in'])
        new_expire_stamp = new_expire_dt.timestamp()
        print(f"new expire date: {new_expire_dt}")
        print(f"new expire : {new_expire_stamp}")
        print(f"recovered expire : {datetime.datetime.fromtimestamp(new_expire_stamp)}")
        
        data = {
            "expires_at": str(new_expire_stamp),
            "access_token": token_info["access_token"],
        }
        write_config(self.config_file, "token_info", data, self.config)
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