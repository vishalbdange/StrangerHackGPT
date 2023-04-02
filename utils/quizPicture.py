import requests
from api.uploadMedia import uploadMedia

def getQuizPicture(givenUrl):
    img_url = givenUrl
    response = requests.get(img_url)
    if response.status_code:
        fp = open('static/quizMedia/quizImage.png', 'wb')
        fp.write(response.content)
        fp.close()
    mediaId,mediaType = uploadMedia('quizImage.png','static/quizMedia/quizImage.png','png')
    return mediaId