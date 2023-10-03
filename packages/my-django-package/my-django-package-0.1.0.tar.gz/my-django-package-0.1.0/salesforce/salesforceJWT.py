import jwt
from pathlib import Path
from . import salesforce_settings
import requests
import time
 
#Set Salesforce JWT Headers
jwtHeaders = {
    "alg" : "RS256",
    "typ" : "JWT"
}

#Set Salesforce JWT Payload
jwtPayload = {
    "iss" : salesforce_settings.SALESFORCE_CONSUMER_KEY,
    "sub" : salesforce_settings.SALESFORCE_USERNAME,
    "aud" : "https://login.salesforce.com",
    # "aud" : "https://test.salesforce.com",
    "exp" : time.time() #currentTime Stamp "1657530866" 
}

#Import your Key
key = Path(salesforce_settings.SALESFORCE_PRIVATEKEY_FILE).read_text().encode('utf-8')

#Contruct & Sign the JWT
encodedJWT = jwt.encode(jwtPayload,key,algorithm='RS256',headers=jwtHeaders)
print("encodedJWT",encodedJWT)