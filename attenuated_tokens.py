import base64
from operator import truediv
import jwt
import json
import hashlib


def new_permission_valid(decoded_payload_data, new_permission):
    return True #TO DO

def derive_key(value):
    return hashlib.sha256(value.encode()).hexdigest()

#TO DO: don't store header, just use parent algorithm. When decoding the most attenuated token contains the algorithm everyone else used.
#This limits using different algorithms, which is really not necessary, and shrinks attenuated tokens considerably.
def attenuate_jwt(parent_token, new_permission):
    
    #not really needed, just to make sure the parent is properly created and not expired
    #try:     
    #    decoded_payload_data = jwt.decode(token, api_key, algorithms=['HS256'])
    #except:
    #    print("invalid token") 
    #    return

    #TO DO handle exception in the invoker
    decoded = jwt.api_jwt.decode_complete(parent_token, options={"verify_signature": False})

    if not new_permission_valid(decoded["payload"], new_permission):
        raise Exception("New Permissions are broader than original")

    attenuated_payload_data = {
        #"sub" : decoded["payload"]['sub'],
        "access" : new_permission,
        "parent_payload" : decoded["payload"]
    }
    
    derived_key = derive_key(parent_token)

    attenuated_jwt = jwt.encode(
        payload=attenuated_payload_data,
        key=derived_key,
        algorithm=decoded["header"]["alg"]
    )

    return attenuated_jwt



#TO DO check for permission errors and expiration dates.
#TO DO 
#recreates the final attenuated token unwrapping until it gets to the original JWT.
def recreate_attenuated_token(decoded_payload, base_key, algorithms):

    #TO DO can we just do a JSON load on the payload, this is ugly. Maybe the recursion should happen on payloads and not the final attenuated JWT. 
    
    if "parent_payload" in decoded_payload:
        print("it's an attenuated token, key needs to be derived")
        key = recreate_attenuated_token(decoded_payload["parent_payload"], base_key, algorithms)
    else:
        key = base_key
        #base case
        print("base case: derive first key")

    #TO DO: check if validating it's not expired, if not a decode is required.
    base_token = jwt.encode(
        payload = decoded_payload,
        key=key,
        #algorithm="HS256"
        algorithm=algorithms[0]
    )
    return derive_key(base_token)


def decode(attenuated_jwt, base_key, algorithms):
    try:     
        decoded_payload_data = jwt.decode(attenuated_jwt, base_key, algorithms)
        print("it's a regular token") 
        return decoded_payload_data
    except:
        decoded_payload = jwt.decode(attenuated_jwt, options={"verify_signature": False})
        jwt_hash = recreate_attenuated_token(decoded_payload, base_key, algorithms)
        if jwt_hash == derive_key(attenuated_jwt):
            return decoded_payload
        else:
            return None #maybe raise an exception?
