import requests

url = "https://iqwhatsapp.airtel.in:443/gateway/airtel-xchange/basic/whatsapp-manager/v1/session/media"

def uploadMedia(mediaName, mediaLocation, fileType):
    
    if fileType == 'png':
        fileType = 'image/png'
        mediaType = "IMAGE"
        
    if fileType == 'jpg' or fileType == 'jpeg':
        fileType = 'image/jpeg'
        mediaType = "IMAGE"
    
    if fileType == 'pdf':
        fileType = 'application/pdf'
        mediaType = "DOCUMENT"
    
    if fileType == 'csv':
        fileType = 'text/csv'
        mediaType = "DOCUMENT"
    
    if fileType == 'docx':
        fileType = 'application/msword'
        mediaType = "DOCUMENT"
        
    if fileType == 'mp4':
        fileType = 'video/mp4'
        mediaType = "VIDEO" 
        
    if fileType == '3gpp':
        fileType = 'video/3gpp'
        mediaType = "VIDEO" 
        
    if fileType == 'aac':
        fileType = 'audio/aac'
        mediaType = "AUDIO"
    
    if fileType == 'mp3':
        fileType = 'audio/mp4'
        mediaType = "AUDIO"
    
    if fileType == 'amr':
        fileType = 'audio/amr'
        mediaType = "AUDIO"
    
    if fileType == 'ogg':
        fileType = 'audio/ogg'
        mediaType = "AUDIO"
    
    payload={'type': mediaType,
    'businessId': 'Hackathon3_8904587734'}
    files=[
        ('file',(mediaName,open(mediaLocation,'rb'), fileType))
    ]
    headers = {
        'Authorization': 'Basic QUlSVEVMX0RJR19MeEk4VFVLOGVLZnRCa3lQdWlmTDoxeipMVTZLTjxrenNMPytiVzM2'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(str(''.join(filter(str.isdigit, response.text))))
    print(response.text)
    
    mediaId =  str(''.join(filter(str.isdigit, response.text)))
    print('MEDIAAA: ' +  mediaId)
    return mediaId, mediaType
    
