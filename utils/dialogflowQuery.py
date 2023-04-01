import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
load_dotenv()

# set Google Application credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'dialogflow_private_key.json' # absolute path of JSON file


# set Dialogflow project credentials
DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = os.environ['SESSION_ID']
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)


def respond(message):
    response = MessagingResponse()
    response.message(message)
    print(str(response))
    return str(response)

def dialogflow_query(message):
    text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)  
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        # print("Query text:", response.query_result.query_text)
        # print("Detected intent:", response.query_result.intent.display_name)
        # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        # print("Fulfillment text:", response.query_result.fulfillment_text)
        # print(response.query_result.fulfillment_text)
        # index(response.query_result.query_text)
        # mediaUrl = student_progress(db)
        respond(response.query_result.fulfillment_text)
        return response 
    except InvalidArgument:
        raise