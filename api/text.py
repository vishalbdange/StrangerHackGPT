import requests
import json
from deep_translator import GoogleTranslator

url = "https://iqwhatsapp.airtel.in:443/gateway/airtel-xchange/basic/whatsapp-manager/v1/session/send/text"

def sendText(receiver, langId, text, sessionId):
    if langId != 'en':
        text = GoogleTranslator(source="en", target=langId).translate(text)
        
    payload = json.dumps({
        "sessionId": sessionId,
        "to": receiver,
        "from": "918904587734",
        "message": {
            "text": text
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic QUlSVEVMX0RJR19MeEk4VFVLOGVLZnRCa3lQdWlmTDoxeipMVTZLTjxrenNMPytiVzM2'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


