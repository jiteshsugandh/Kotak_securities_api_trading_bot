import Credentials as C
from ks_api_client import ks_api
import requests, json
 

# Defining the host is optional and defaults to https://tradeapi.kotaksecurities.com/apim
# See configuration.py for a list of all supported configuration parameters.
client = ks_api.KSTradeApi(access_token = C.access_token, userid = C.userid, \
                consumer_key = C.consumer_key, ip = C.ip, app_id = C.app_id)

client.login(password = C.password)

def login(client,consumer_key,access_token,app_id,user_id,password):
    headers={'accept':'application/json','consumerKey':consumer_key,'ip':'127.0.0.1','appId':app_id,'Content-Type':'application/json','Authorization':"Bearer "+access_token}
    data=json.dumps({'userid':user_id,'password':password})
    response= requests.post("https://tradeapi.kotaksecurities.com/apim/session/1.0/session/login/userid",headers=headers,data=data).json()
    url = "https://tradeapi.kotaksecurities.com/apim/session/1.0/session/2FA/oneTimeToken"
    headers["oneTimeToken"] = response['Success']['oneTimeToken']
    client.one_time_token=headers['oneTimeToken']
    data = json.dumps({"userid":user_id})
    resp = requests.post(url, headers=headers, data=data).json()
    client.session_token=resp['success']['sessionToken']
    #print("Session Token ",client.session_token)
    #print("Loged In  Successfully")
    return client

login(client,C.consumer_key,C.access_token,C.app_id,C.userid,C.password)