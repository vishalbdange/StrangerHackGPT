
from api.text import sendText
from api.oneButton import sendOneButton
from api.help import sendHelp


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
razorpay_key = os.environ['RAZORPAY_KEY_ID']
razorpay_secret = os.environ['RAZORPAY_KEY_SECRET']

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

    if request_data["message"]["type"] == "order":
        userCatalog = db['test'].find_one({'_id':  request_data['from']})
        if userCatalog is not None:
            WaId = request_data["from"]
            if len(request_data["message"]["order"]["product_items"]) < 1:
                print('No Course Selected')
                sendText(WaId,'en',"No Course Selected", request_data['sessionId'])
                pass
            else:
                # fetch coursera id of current user
                userInfo = db['test'].find_one({'_id': WaId})
                print(userInfo)
                if userInfo["courseraId"] == '':
                    print('Coursera Id Not There')
                    mediaIdProfile, mediaTypeProfile = uploadMedia('courseraProfileHelp.jpg', 'static/helpMedia/courseraProfileHelp.jpg', 'jpg')
                    sendText(WaId, userInfo['langId'], "It looks like you haven't submitted a profile URL link.🤔 Please make sure that you submit the Coursera Profile link that is displayed when you visit your profile in our portal. To submit the link, just *text* it here, I will update it right away! For reference, please consider the image attached!\n Just copy and paste your profile URL here in our chat, for example, *Here is my profile ID https://www.coursera.org/user/4142eae2bd3c41fbec7d346083fa4f13*", request_data['sessionId'])
                    sendMedia(WaId, mediaIdProfile, mediaTypeProfile, request_data['sessionId'])

                    # send message to add coursera id of the user
                    pass
                else:
                    # Get Requested Courses from cart
                    requestedCourses = request_data["message"]["order"]["product_items"]
                    alreadyRegisteredCourses = [x["courseId"] for x in userInfo["courses"]]
                    print("already registered", alreadyRegisteredCourses)
                    alreadyRegisteredFlag = 0

                    courseDetails = []
                    totalFees = 0

                    for item in requestedCourses:
                        retail_id = item["product_retailer_id"]
                        print(retail_id)

                        courseData = db['course'].find_one({"catalogProductId": retail_id})
                        print("course data")
                        print(courseData)

                        # check if alredy paid or not
                        if courseData["_id"] in alreadyRegisteredCourses:
                            alreadyRegisteredFlag = 1
                            break
                        else:
                            today = date.today()

                            if courseData["courseType"] == "static":
                                courseTemp = {
                                    "courseId": courseData["_id"],
                                    "courseType": "static",
                                    "courseFees": courseData["courseFees"],
                                    "courseStartDate": str(today),
                                    "courseEndDate": str(today + timedelta(weeks=courseData["courseDuration"])),
                                    "quantity": item["quantity"],
                                    "courseLink": courseData["courseLink"]
                                }
                            else:
                                courseTemp = {
                                    "courseId": courseData["_id"],
                                    "courseType": "dynamic",
                                    "courseFees": courseData["courseFees"],
                                    "courseStartDate": courseData["courseStart"],
                                    "courseEndDate": courseData["courseEnd"],
                                    "quantity": item["quantity"],
                                    "courseLink": courseData["courseLink"]
                                }
                            courseDetails.append(courseTemp)
                            totalFees += courseData["courseFees"]

                    print("Course Details")
                    print(courseDetails)


                    if alreadyRegisteredFlag == 1:
                        # course already registered message to user
                        print('course already registered message to user')
                        sendText(WaId,userInfo['langId'],"Course(s) already registered! Why not explore some more courses? 😋", request_data['sessionId'])
                        sendCatalog(request_data['from'],userInfo['langId'],request_data['sessionId'])
                    else:
                        # send payment link
                        sendText(WaId,'en',"https://vikings.onrender.com//register-for-course/"+WaId, request_data['sessionId'])
                        cartFlag = db["cart"].find_one({'_id': WaId})
                        if cartFlag is not None:
                            db["cart"].delete_one({'_id': WaId})

                        db['cart'].insert_one({
                            '_id': WaId,
                            'courseDetails': courseDetails,
                            'totalFees': totalFees
                        })
                        print("finally the end")
            return ''
        else:
            sendText(request_data['from'], 'en',"You need to register first to buy our courses! Do not worry! It won't take much time!⚡ ", request_data['sessionId'])
            sendTwoButton( request_data['from'], 'en', "Register right now! It will be the best decision for a brighter future! 🌎", ["register", "roam"], ["Register right now!", "Just exploring!"], request_data['sessionId'])
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

@app.route('/register-for-course/<WaId>')
def form(WaId):
    global _id, name
    _id = WaId
    userInfo = db['test'].find_one({"_id": WaId})

    cartInfo = db['cart'].find_one({"_id": WaId})

    courseDetails = []
    totalFees = 0

    if cartInfo is not None:
        courseDetails = cartInfo["courseDetails"]
        totalFees = cartInfo["totalFees"]
    else:
        # send message to user
        sendText(WaId,'en', "Your cart is empty 🛒", '757575757575757575')
        return 'Cart Empty'

    print(totalFees)
    print(courseDetails)

    # discount checking
    offersAvailable = []
    offers = userInfo["offersAvailed"]
    print(offers)
    for o in offers:
        if o["discountRedeemed"] == "false":
            discountPercent = db['discounts'].find_one({'_id': o["discountId"]})
            offersAvailable.append(str(o["discountId"]) + ' - ' + str(int((1-float(discountPercent["discountOffered"]))*100)) + "%")

    print(offersAvailable)

    return render_template('payment_form.html', name=userInfo["name"], mobile=_id, courses=courseDetails, coursesLen=len(courseDetails), offers=offersAvailable, offersLen=len(offersAvailable))


@app.route('/pay', methods=['POST'])
def pay():
    if request.method == "POST":
        WaId = request.form['mobile']
        WaId = WaId[1:3] + WaId[4:]
        session['contact'] = WaId

        userInfo = db['test'].find_one({"_id": WaId})
        cartInfo = db['cart'].find_one({"_id": WaId})

        if cartInfo is not None:
            courseDetails = cartInfo["courseDetails"]
            totalFees = cartInfo["totalFees"]
        else:
            # send message to user
            return 'Cart Empty'

        offer = request.form['offers']
        if offer == "none":
            session['offer'] = 'None'
            offer = 1
        else:
            session['offer'] = offer.split(' - ')[0]
            offer = offer.split(' - ')[1][:-1]
        discountAmount = totalFees*int(offer)/100
        offer = 1 - int(offer)/100
        print('offer', offer)

        feesToBePaid = totalFees*offer

        client = razorpay.Client(auth=(razorpay_key, razorpay_secret))
        notes = {
            'name': userInfo["name"],
            'email': userInfo["email"],
            'contact': WaId,
            'totalFees': totalFees,
            'discountAmount': discountAmount,
            'offer': offer,
            'feesToBePaid': feesToBePaid
        }

        session["amount"] = feesToBePaid
        payment = client.order.create({"amount": int(feesToBePaid)*100,
            "currency": "INR",
            "payment_capture": 1,
            "notes": notes})
        return render_template('pay.html', payment=payment, razorpay_key=razorpay_key, course=courseDetails, courseLen=len(courseDetails))


@app.route('/healthz')
def healthz():
    return ''


@app.route('/success', methods=['POST'])
def success():
    if request.method == "POST":
        print('Razorpay Payment ID: ' + request.form['razorpay_payment_id'])
        print('Razorpay Order ID: ' + request.form['razorpay_order_id'])
        print('Razorpay Signature: ' + request.form['razorpay_signature'])
        print(request.form)

        WaId = session["contact"]
        amount = session["amount"]

        userInfo = db['test'].find_one({"_id": WaId})
        cartInfo = db['cart'].find_one({"_id": WaId})

        if cartInfo is not None:
            courseDetails = cartInfo["courseDetails"]
            totalFees = cartInfo["totalFees"]
        else:
            # send message to user
            sendText(WaId,'en', "Your cart is empty 🛒", '757575757575757575')
            return 'Cart Empty'

        res = []
        messageCourse = []
        json = {}
        for c in courseDetails:
            if c["courseType"] == "static":
                messageCourse.append(c["courseId"])
                json = {
                    "courseId": c["courseId"],
                    "courseType": c["courseType"],
                    "courseStartDate": c["courseStartDate"],
                    "courseEndDate": c["courseEndDate"],
                    "courseQuizzes": [],
                    "coursePayment": True
                }
            if c["courseType"] == "dynamic":
                messageCourse.append(c["courseId"])
                json = {
                    "courseId": c["courseId"],
                    "courseType": c["courseType"],
                    "courseStartDate": c["courseStartDate"],
                    "courseEndDate": c["courseEndDate"],
                    "courseFeedback": '',
                    "coursePayment": True
                }
            res.append(json)

        res = userInfo["courses"] + res

        db["test"].update_one({
                '_id': WaId
            }, {
                '$set': {
                    'courses': res
                }
            })

        db["cart"].delete_one({'_id': WaId})

        get_receipt(courseDetails, session['amount'])
        mediaId, mediaType = uploadMedia('receipt.pdf', 'static/paymentMedia/receipt.pdf', 'pdf')
        print(mediaId, mediaType)
        sendMedia(WaId, mediaId, mediaType, '7575757575757575')

        if session['offer'] != 'None':
            db['test'].update_one({'_id': WaId, 'offersAvailed.discountId': session['offer']}, {'$set': {'offersAvailed.$[offersAvailed].discountRedeemed': "true"}}, array_filters=[{"offersAvailed.discountId": {"$eq": session['offer']}}], upsert=True)
            print('update done')

        wa_message = ''
        if len(messageCourse) != 0:
            wa_message = ', '.join(messageCourse) + ' are static courses.\nYou can attempt quizzes for such courses and bag rewards! Use *Quiz me* for example!\n\n'

        for c in courseDetails:
            wa_message += '\nVisit the course *'+ c['courseId'] + '* at '+c['courseLink']
        wa_message += '\nYou can also check for progress of individual courses!\nText *Progress me* for example! \n Need more resources? Try texting *I need study resources* for books and notes!'
        sendText(WaId,'en', wa_message, '757575757575757575')

        # remove all sessions values
        session.pop('contact', None)
        session.pop('offer', None)
        session.pop('amount', None)

        return render_template('success.html', payment_id=request.form['razorpay_payment_id'], contact=WaId, email = userInfo["email"], amount=amount)


if __name__ == '__main__':
  app.run(debug=False)
