import random, witai, TimeTableDatabase, time, TimeTableScraper, os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:

            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                sender_id = message['sender']['id']
                recipient_id = message['sender']['id']
                if message['message'].get('text'):

                    messaging_text = message['message']['text']

                    entity, value = witai.wit_response(messaging_text)
                    print("wit ai:")
                    print(entity, value)
                    get_message(sender_id, entity, value)

    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message(sender_id, entity, value):
    response = ""
    DB_RESULT_TRUE = False
    print("Deciphering intent...")
    
    try:
        print(type(entity))
        if 'help_type' in entity:
            send_message(sender_id, "Type in\n do I have lectures on Monday,\n or do I have labs today.")
    except:
        print("Help handling failed...")

    if len(entity) > 1 or 'help_type' in entity: #Checks if there is a class/lecture intent and date time intent
        print("Passing...")
    else:
        send_message(sender_id, "Please retype the message more clearly.") #\n Type help to see what I can do for you.")
        print("Less than 2 intents in statements, returning NONE.")
        return None

    try:
        
        if 'class_type' in entity or 'lecture_check' in entity:
            # and if class_type is in the classes already in DB
            ChooseMessage(sender_id, entity, value, "lectures")

        elif 'clinic_check' in entity:
            #response = "Hold on. Let me check if you have clinics."
            ChooseMessage(sender_id, entity, value, "clinics")
            send_message(sender_id, response)

        elif 'lab_check' in entity:
            #response = "Hold on. Let me check if you have labs."
            ChooseMessage(sender_id, entity, value, "labs")
            #send_message(sender_id, response)

    except:
        print("Get message error")
        TimeTableDatabase.ExceptionInfo()
        pass


def ChooseMessage(sender_id, entity, value, classtypestring):
    response = "Hold on. \n Let me check if you have %s." % classtypestring
    DB_RESULT_TRUE = False
    send_message(sender_id, response)
    print("Getting correct user response...")
    try:
        print(value.index("u'datetime"))
        print("Getting day of request... (%s)" % str(value[(value.index("u'datetime"))].strftime('%A')))
        if 'class_check' in entity or 'lecture_check' in entity:
            results = TimeTableDatabase.GetLecturesOnDay(value[1].strftime('%A'))
        elif 'lab_check' in entity or 'clinic_check' in entity:
            results = TimeTableDatabase.GetSpecificClassType("Lab_Practical", value[(value.index("u'datetime"))].strftime('%A'))
            print(type(entity))

        if len(results) != 0:
            DB_RESULT_TRUE = True
            parsedresults = TimeTableDatabase.parse_results(results)
            #print("Parsed results:")
            #print(parsedresults)
    except:
        print("Lecture fetching exception")
        TimeTableDatabase.ExceptionInfo()
        send_message(sender_id, "Error fetching lectures. \n Please try again later.")

    if DB_RESULT_TRUE == True:
        #response = ""
        for i in range(0, len(results)):
            response = ""
            #print(type(parse_results[i]))
            for y in range(0, len(parsedresults[i])):
                if y == 2:
                    response += parsedresults[i][y] + " to "
                else:
                    response += parsedresults[i][y] + "\n"
            response.replace("[", "")
            response.replace("]", "")
            send_message(sender_id, response)#str(parsedresults[i]) + "\n\n")
    else:
        send_message(sender_id, "No classes on %s" % str(value[1].strftime('%A')))

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
