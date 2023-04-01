from api.courseraProfile import getCourseraProfile
from utils.db import db
from api.text import sendText
from api.uploadMedia import uploadMedia 
from api.media import sendMedia
from api.catalog import sendCatalog

def checkProfile(receiver, langId, courseraProfileUrl, sessionId):
    statusCode = getCourseraProfile(courseraProfileUrl)
    print(type(statusCode))
    if statusCode == '200' or statusCode == 200:
        db["test"].update_one({ '_id': receiver }, { "$set": { 'courseraId': courseraProfileUrl }} )
        sendText(receiver, langId, "Awesome!🎯 We have noted your coursera profile successfully! Happy shopping!", sessionId)
        sendCatalog(receiver, langId,sessionId)
        return ''
    
    mediaId, mediaType = uploadMedia('courseraProfileHelp.jpg', 'static/helpMedia/courseraProfileHelp.jpg', 'jpg')
    print(mediaId, mediaType)
    sendText(receiver, langId, "It looks like you submitted an incorrect profile URL link.🤔 Please make sure that you submit the correct Coursera Profile link that is displayed when you visit your profile in our portal. To submit the link, just *text* it here, I will update it right away! For reference, please consider the image attached! \n Just copy and paste your profile URL here in our chat, for example, *Here is my profile ID https://www.coursera.org/user/4142eae2bd3c41fbec7d346083fa4f13*", sessionId)
    sendMedia(receiver, mediaId, mediaType, sessionId)
    
    return ''