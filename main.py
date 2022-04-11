from operator import truediv
import jwt
import json
import hashlib

API_KEY = "456bcecd4c5ef7f566a066cb8d2ed522fca23a9e61ee7c80677b6356fd5d3757"
DUMMY_SIGNATURE = ".dummy_signature"


access_scheme = { "admin": 
                    {"read_write": 
                        {"read": "true",
                        "write": "true"
                        }
                    },
                    "delete": "true",
                    "update": "true",
                    "create": "true"
                }


#print(access_scheme.get("read_write"))

resource_scheme = {
    "all": ["A", "B", "C"]
}

payload_data = {
    "sub": "4242",
    "access":
        {
            "role": "admin",
            "resource": "all"
        }
}


payload_data2 = {
    "sub": "4242",
    "access": [
        {
            "role": "admin",
            "resource": "all"
        },
        {
            "role": "admin",
            "resource": "A"
        }
    ]
}

token = jwt.encode(
    payload=payload_data,
    key=API_KEY
)

#print(token)

try:
    decoded_payload_data = jwt.decode(token, API_KEY, algorithms=['HS256'])
except jwt.ExpiredSignatureError as error:
    print("token expired")
    exit()
#TO DO except for invalid key...

new_permission = {
            "role": "read",
            "resource": "all"
        }


#decoded_payload_data_dict = json.loads(decoded_payload_data)

def validate_new_permission(decoded_payload_data, new_permission):
    return True #TO DO

def derive_key(value):
    return hashlib.sha256(value.encode()).hexdigest()


def attenuate_jwt(token, new_permission):
    try:     
        decoded_payload_data = jwt.decode(token, API_KEY, algorithms=['HS256'])
    except:
        print("invalid token") 
        return

    if not validate_new_permission(decoded_payload_data, new_permission):
        raise Exception("New Permissions are broader than original")


    token_splits = token.split('.') #decode makes sure there are 3 parts
    token_without_signature = token_splits[0] + "." + token_splits[1]
    #print(token_without_signature)

    attenuated_payload_data = {
        "sub" : decoded_payload_data['sub'],
        "access" : new_permission,
        "inherited_payload" : token_without_signature
    }
    

    #derived_key = hashlib.sha256(token.encode()).hexdigest()
    derived_key = derive_key(token)
    #print(derived_key)

    attenuated_jwt = jwt.encode(
        payload=attenuated_payload_data,
        key=derived_key
    )

    return attenuated_jwt



#another wrapper should get the final permissions or error
#returns the key used for each JWT. At the end it returns the fictional K+1 Key, the hash of the attenuated JWT.
#an alternative is to return the 
def validate_token_aux(attenuated_jwt):

    decoded_payload = jwt.decode(attenuated_jwt, options={"verify_signature": False})
    
    if "inherited_payload" in decoded_payload:
        print("it's an attenuated token, key needs to be derived")
        
        #dummy signature is appended so it can be interpreted as a JWT, and decoded without signature validation.
        key = validate_token_aux(decoded_payload["inherited_payload"] + DUMMY_SIGNATURE)
        
        try:     
            decoded_payload_data = jwt.decode(attenuated_jwt, key, algorithms=['HS256'])
            return derive_key(attenuated_jwt)
        except:
            print("invalid token") 
            return "" #TO DO: not sure if None would be better

    
    #base case
    print("base case: derive first key")
    #TO DO each token must validate permissions with it's parent

    base_token = jwt.encode(
        payload = decoded_payload,
        key=API_KEY
    )
    return derive_key(base_token)


def get_payload(attenuated_jwt):
    try:     
        decoded_payload_data = jwt.decode(attenuated_jwt, key, algorithms=['HS256'])
        print("it's a regular token") 
        return decoded_payload_data
    except:
        jwt_hash = validate_token_aux(attenuated_jwt)
        if jwt_hash == derive_key(attenuated_jwt):
            decoded_payload = jwt.decode(attenuated_jwt, options={"verify_signature": False})
            return decoded_payload #maybe inherited_payload should be removed.
        else:
            return None #maybe raise an exception?


attenuated_jwt = attenuate_jwt(token, new_permission)
#print(attenuated_jwt)

print(get_payload(attenuated_jwt))


#https://www.openpolicyagent.org/
json_access_scheme = {
    "role":
        { "admin" :
             [{
                "read_write" : 
                [
                    { 
                        "read" : "read"
                    },
                    {
                        "write" : "write"
                    }
                ]
            },
            {
                "delete" : "delete"
            }]    
        }
    }
