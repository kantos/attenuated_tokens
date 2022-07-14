import jwt
import json
import hashlib

API_KEY = "asd"

payload_data = {
    "sub": "4242",
    "access":
        {
            "role": "admin",
            "resource": "all"
        }
}

token = jwt.encode(
    payload=payload_data,
    key=API_KEY
)


token_splits = token.split('.') #decode makes sure there are 3 parts
token_without_signature = token_splits[0] + "." + token_splits[1] + ".dummy_signature"

#jwt.decode(token, API_KEY, algorithms=['HS256'])   
decoded_payload = jwt.decode(token_without_signature, options={"verify_signature": False})
print(decoded_payload)