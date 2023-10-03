import requests
from . import salesforceJWT
from simple_salesforce import Salesforce
from . import salesforce_settings

salesforceEndpoint = 'https://login.salesforce.com/services/oauth2/token' 
# salesforceEndpoint = 'https://test.salesforce.com/services/oauth2/token' 

salesforceUrlParams = {
    'grant_type' : 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion' :salesforceJWT.encodedJWT
}

response = requests.post(salesforceEndpoint, params=salesforceUrlParams, verify=True)
print (response)

sf = Salesforce(
    username=salesforce_settings.SALESFORCE_USERNAME,
    password=salesforce_settings.SALESFORCE_PASSWORD,
    # security_token= response, #salesforce_settings.SALESFORCE_SECURITY_TOKEN,
    consumer_key=salesforce_settings.SALESFORCE_CONSUMER_KEY,
    # consumer_secret=salesforce_settings.SALESFORCE_CONSUMER_SCRETE
    privatekey_file= salesforce_settings.SALESFORCE_PRIVATEKEY_FILE,
    # domain='test'
)