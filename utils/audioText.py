# Utils
from utils.webSearch import google_search
from api.text import sendText
from api.ngrokAudio import ngrokAudio


def speechToText(requestMediaId, receiver, langId, sessionId):

    mediaId = requestMediaId
    ngrokResponse = ngrokAudio(mediaId)
    if ngrokResponse == False:
        sendText(receiver,'en',"Bug 🐛 \n We do not support these types on Render Server!", sessionId)
        return ''
    if ngrokResponse.status_code == 404 or ngrokResponse.status_code == '404':
        sendText(receiver,'en',"Bug 🐛 \n We do not support these types on Render Server!", sessionId)
        return ''
    textFromImage = ngrokResponse.text
    if textFromImage == '' or ngrokResponse.text is None:
        sendText(receiver,'en',"Sorry! We could not catch that!😢", sessionId)
        return ''
    sendText(receiver,'en',"This is what we have found!", sessionId)
    print(google_search(textFromImage))
    sendText(receiver, langId, google_search(textFromImage), 'sessionId')
    
    return ''

