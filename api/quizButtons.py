import requests
import json

url = "https://iqwhatsapp.airtel.in:443/gateway/airtel-xchange/basic/whatsapp-manager/v1/session/send/interactive/buttons"

def sendQuiz(receiver, quiz, questionNumberString, sessionId):
    payload = json.dumps({
        "sessionId": sessionId,
        "to": receiver,
        "from": "918904587734",
        "message": {
            "text": quiz[questionNumberString]['question']
        },
        "buttons": [
            {
                "tag": "A",
                "title": quiz[questionNumberString]['A']
            },
            {
                "tag": "B",
                "title": quiz[questionNumberString]['B']
            },
            {
                "tag": "C",
                "title": quiz[questionNumberString]['C']
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


def sendButtons_2(receiver, msgText,titles):
    payload = json.dumps({
        "sessionId": "5792547f57a44b358d3f1425dc163b7f",
        "to": receiver,
        "from": "918904587734",
        "message": {
            "text": msgText
        },
        "buttons": [
            {
                "tag": "1",
                "title": titles[0]
            },
            {
                "tag": "2",
                "title": titles[1]
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic QUlSVEVMX0RJR19MeEk4VFVLOGVLZnRCa3lQdWlmTDoxeipMVTZLTjxrenNMPytiVzM2'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
