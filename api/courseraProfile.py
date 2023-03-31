import requests

def getCourseraProfile(url_):
    url = url_
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.status_code)
    
    return response.status_code
