import requests
import json
from deep_translator import GoogleTranslator

url = "https://iqwhatsapp.airtel.in:443/gateway/airtel-xchange/basic/whatsapp-manager/v1/session/send/interactive/buttons"

def sendTwoButton(receiver, langId, text, tag, title, sessionId):
    if langId != 'en':
        text = GoogleTranslator(source="en", target=langId).translate(text)
        title[0] = GoogleTranslator(source="en", target=langId).translate(title[0]) + '(' + tag[0] +')'
        title[1] = GoogleTranslator(source="en", target=langId).translate(title[1]) + '(' + tag[1] +')'
        
    payload = json.dumps({
        "sessionId": sessionId,
        "to": receiver,
        "from": "918904587734",
        "message": {
            "text": text
        },
        "buttons": [
            {
                "tag": tag[0],
                "title": title[0]
            }, 
            {
                "tag": tag[1],
                "title": title[1]
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic QUlSVEVMX0RJR19MeEk4VFVLOGVLZnRCa3lQdWlmTDoxeipMVTZLTjxrenNMPytiVzM2'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

# 919820860959
