import requests
from utils.db import db

def ngrokImage(mediaId):
    ngrok = db['config'].find_one({'_id': 'ngrok'})
    ngrokLink = ngrok['ngrokLink']
    
    if ngrokLink == '':
        return False
    url = ngrokLink + "/image"

    payload={'mediaId': mediaId}
    files=[

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response)
    return response
