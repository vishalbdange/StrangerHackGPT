import requests
import json
from deep_translator import GoogleTranslator

url = "https://iqwhatsapp.airtel.in:443/gateway/airtel-xchange/basic/whatsapp-manager/v1/session/send/product/multiple"

def sendCatalog(receiver, langId, sessionId):
    text_ = " Start, switch, or advance your career with amazing courses, Professional Certificates, and degrees from world-class universities and companies! 🚀"
    if langId != 'en':
        text_ = GoogleTranslator(source="en", target=langId).translate(text_)
    
    text = "Coursera Catalog!🎊" + text_
    payload = json.dumps({
    "sessionId": sessionId,
    "to": receiver,
    "from": "918904587734",
    "message": {
        "text": text
    },
    "catalog": {
        "heading": "Courses",
        "catalogId": "1274826006422621",
        "sections": [
        {
            "heading": "History",
            "products": [
                "1ruz900fi1"
            ]
        },
        {
            "heading": "Maths",
            "products": [
                "xrmdx16tsv"
            ]
        },
        {
            "heading": "Science",
            "products": [
                "y1bwippss9"
            ]
        },
        {
            "heading": "English",
            "products": [
                "uujarveydy"
            ]
        },
        {
            "heading": "Geography",
            "products": [
                "ky6ok1soz8"
            ]
        },
        {
            "heading": "Psychology",
            "products": [
                "njl5b6n1ji"
            ]
        },
        {
            "heading": "Python",
            "products": [
                "hqetsudfju"
            ]
        },
        {
            "heading": "Economics",
            "products": [
                "0l0645vhcc"
            ]
        }
        ]
    }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic QUlSVEVMX0RJR19MeEk4VFVLOGVLZnRCa3lQdWlmTDoxeipMVTZLTjxrenNMPytiVzM2'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
