import random
from api.threeButton import sendThreeButton


def organisationIntroduction(receiver, langId, sessionId):
    
    organisation_init_text = ["We are glad you want to know more about us! Please tell me what would you like to know from the options? 😌",
                        "Our organisation has been reputed since a long time!😯 Please select one of the following options now!",
                        "Let me introduce you to our organisation! 🎉 Discover more about us, what would you like to know?",
                        "We love making potential world leaders aware about our family! 🎖️ Click on what you would like to know about!"]
    sendThreeButton(receiver, langId, organisation_init_text[random.randint(0, 3)], ["org-history", "org-vision", "org-contact"], ["Our History!", "Our Vision!", "Visit us!"], sessionId)