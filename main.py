 
from api.text import sendText
from api.oneButton import sendOneButton
 

# Extra imports
import pymongo as pymongo
import os
import json
import random
from deep_translator import GoogleTranslator
import langid
 

load_dotenv()

# For payment
import razorpay
 
# creating the Flask object
app = Flask(__name__)
app.secret_key = b'delph@!#78d%'


@app.route('/', methods=['POST'])
def reply():
    request_data = json.loads(request.data)
    print(request_data)
    
    if "businessId" not in request_data:
        return ''
    message_ = ''
    
    #   #___Testing____
    # request_data = {
    #     'from': request.form.get('WaId'),
    #     'sessionId': '7575757575757',
    #     'message': {
    #         'text': {
    #             'body':request.form.get('Body')
    #         },
    #         'type': 'text'
    #     } 
    # }
    # # ___________
    
    if request_data['from'] == '919870613280':
        
        print("Admin time")
        conditionTitle = ((request_data['message']['text']['body']).split(",")[0]).strip().lower()
        
        if conditionTitle == 'promotion':
            courseName_ = (request_data['message']['text']['body']).split(",")[1]
            courseLink_ = (request_data['message']['text']['body']).split(",")[2]
            for document in db['test'].find({}):
                sendPromotion(document.get("_id"), document.get("langId"), courseName_, courseLink_)
            return ''

        
        if conditionTitle == 'ngrok':
            ngrokSet = ((request_data['message']['text']['body']).split(",")[1]).lower()
            if ngrokSet == 'set':
                ngrokLink = ((request_data['message']['text']['body']).split(",")[2]).strip()
                db['config'].update_one({'_id': 'ngrok'}, { "$set": {'ngrokLink': ngrokLink}})
                sendText('919870613280', 'en', "ngrok is set", request_data['sessionId'])
                return ''
            
            if ngrokSet == 'clear' or ngrokSet != 'set':
                db['config'].update_one({'_id': 'ngrok'}, { "$set": {'ngrokLink': ''}})
                sendText('919870613280', 'en', "ngrok is cleared", request_data['sessionId'])
                return ''
        
        if conditionTitle == 'class-absent':
            absentStudent = ((request_data['message']['text']['body']).split(",")[1]).strip()
            absentUserData = db['test'].find_one({'_id': absentStudent})
            sendText(absentStudent, absentUserData['langId'], 'You missed your class today! No worries, you can access the recordings and notes by texting *I need resources*!', request_data['sessionId'])
            return ''
        
        if conditionTitle == 'class-start':
            courseName_ = (((request_data['message']['text']['body']).split(",")[1]).strip()).lower()

            # for document in db['test'].find({'$and':[{'courses.courseId':courseName_}, {'courses.courseFeedback': {"$lt": d}}]}):
            for document in db['test'].find({'courses.courseId':courseName_}):
                # if document.get('course') is not None or len(document.get('course')) != 0:
                sendText(document.get('_id'), document.get("langId"), 'The class for the course - ' + courseName_+' is starting in a few minutes! Here is the link for today!' , request_data['sessionId'])
                sendText(document.get('_id'), 'en', 'https://meet.google.com/kkr-ndxk-kdg' ,  request_data['sessionId'])
                
            return ''
        
        return ''
    
 
    langId = langid.classify(message_)[0]
    if langId != 'en':
        message = GoogleTranslator(
            source="auto", target="en").translate(message_)
    else:
        message = message_
    response_df = dialogflow_query(message)

    user = db['test'].find_one({'_id':  request_data['from']})

  


    return ''

