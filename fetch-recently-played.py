from python.utils.authentication import Authenticator

auth = Authenticator("./env.conf")

# print(auth.__client_id)
# print(auth.__client_secret)

print(auth.refresh_access_token())
print(auth.is_token_near_expires_in_15_min())