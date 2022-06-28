from operator import truediv
import jwt
import json
import attenuated_tokens

API_KEY = "456bcecd4c5ef7f566a066cb8d2ed522fca23a9e61ee7c80677b6356fd5d3757"


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
#print(token.split('.')[1])

#test basic decode
try:
    decoded_payload_data = jwt.decode(token, API_KEY, algorithms=['HS256'])
except jwt.ExpiredSignatureError as error:
    print("token expired")
    exit()
#TO DO except for invalid key...

#test attenuation with new permission
new_permission = {
            "role": "read",
            "resource": "all"
        }

attenuated_jwt = attenuated_tokens.attenuate_jwt(token, new_permission)
attenuated_jwt2 = attenuated_tokens.attenuate_jwt(attenuated_jwt, new_permission)
attenuated_jwt3 = attenuated_tokens.attenuate_jwt(attenuated_jwt2, new_permission)

#print(attenuated_jwt)
print(attenuated_jwt3)

print(attenuated_tokens.decode(attenuated_jwt3, API_KEY, algorithms=['HS256']))

#decoded_payload_data_dict = json.loads(decoded_payload_data)