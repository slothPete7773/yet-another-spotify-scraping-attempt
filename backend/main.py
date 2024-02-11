from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from utils.authentication import write_config
from configparser import ConfigParser



app = FastAPI()

@app.get("/")
def _root(): 
    return {
        "greet": "hello-world"
    }

@app.get("/authorization")
async def _authorization(code: str=None):
    # try:
    if code is not None:
        config = ConfigParser()
        config_filepath = "backend/utils/env.conf"
        token_info_dict = {
                "code": code
            }
        write_config(config_filepath, "token_info", token_info_dict, config)
        return {
            # "access_code": code,
            "state": 200,
        }
    else:
        return {
            "state": "error"
        }
        # access_token = spotify_auth.get_access_token(code)
        # return RedirectResponse(url=f"/?token={access_token}")
    # else: RedirectResponse(url=f"/")