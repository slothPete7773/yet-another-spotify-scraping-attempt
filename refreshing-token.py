from datetime import datetime
from utils.authentication import Authenticator

with open("log/refreshing-token.txt", "a") as file:
    auth = Authenticator("env.conf")
    is_near_expire = auth.is_token_near_expires_in_15_min()
    if is_near_expire:
        refresh_token = auth.refresh_access_token()
        # print(refresh_token)
        # if refresh_token['state'] == 0:
        #     refresh_text = f"Refresh token before it expired @ {datetime.now()} || new expire timestamp: {refresh_token['token_info']['expires_at']} | {datetime.fromtimestamp(refresh_token['token_info']['expires_at'])} \n"
        #     file.write(refresh_text)
        #     exit()

        # text = f"Token is nearly expired @ {datetime.now()}\n"
        # text = f"Hello World @ {datetime.now()}\n"
        # with open("")
        # file.write(text)
        exit()
    else:
        text = f"Token is not near expired @ {datetime.now()}\n"
        # text = f"Hello World @ {datetime.now()}\n"
        # with open("")
        file.write(text)
        exit()
