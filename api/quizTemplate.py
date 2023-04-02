import requests
import json
from deep_translator import GoogleTranslator

url = "https://iqwhatsapp.airtel.in:443/gateway/airtel-xchange/basic/whatsapp-manager/v1/template/send"


def sendQuizQuestion(receiver, langId, question, options, imageId):
    if langId != 'en':
        question = GoogleTranslator(source="en", target=langId).translate(question)
        options[0] = GoogleTranslator(source="en", target=langId).translate(options[0]) 
        options[1] = GoogleTranslator(source="en", target=langId).translate(options[1]) 
        options[2] = GoogleTranslator(source="en", target=langId).translate(options[2]) 
    
    quizPlate = question + ' A: ' + options[0] + ' B: ' + options[1] + ' C: ' + options[2] + ''
    quizPlate = quizPlate
    print(quizPlate)
    
    payload = json.dumps({
    "templateId": "797ff1d9-ca7c-410a-802e-b6eca976be1e",
    "to": receiver,
    "from": "918904587734",
    "message": {
        "variables": [
            quizPlate
        ],
        "payload": [
            "A",
            "B",
            "C"
        ]
    },
    "mediaAttachment": {
        "type": "IMAGE",
        "id": imageId
    },
    "filterBlacklistNumbers": False
    })
    headers = {
        'X-Correlation-Id': 'abcd',
        'X-Date': '{{date}}',
        'Authorization': 'Basic QUlSVEVMX0RJR19MeEk4VFVLOGVLZnRCa3lQdWlmTDoxeipMVTZLTjxrenNMPytiVzM2',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
