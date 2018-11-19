import random, witai, TimeTableDatabase
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = ''
VERIFY_TOKEN = ''
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
    try:
        if entity[0] == 'class_type': # and if class_type is in the classes already in DB
            response = "Hold on. Let me check if you have {0}".format(str(value)) # Add a spell check
            send_message(sender_id, response)
            try:
                print("Getting day of request...")
                results = TimeTableDatabase.GetLecturesOnDay(value[1].strftime('%A'))

                if len(results) > 0:
                    for i in range(0, len(results)):
                        send_message(sender_id, results[i])
                else:
                    send_message(sender_id, "No classes on that day")
            except:
                print("Class check error")
                pass

        elif entity[0] == 'lecture_check':
            response = "Hold on. Let me check if you have lectures."
            send_message(sender_id, response)
            try:
                print("Getting day of request...")
                results = TimeTableDatabase.GetLecturesOnDay(value[1].strftime('%A'))
                #print(results)
                #send_message(sender_id, len(results))
                #send_message(sender_id, results[0])

                while i < len(results):
                    placeholder = results[i]
                    send_message(sender_id, placeholder)
                    i += 1

                if len(results) > 0:
                    for i in range(0, len(results)):
                        send_message(sender_id, results[i])
                else:
                    send_message(sender_id, "No classes on that day")

            except:
                print("lecture check error")
                TimeTableDatabase.ExceptionInfo()
                pass

        elif entity[0] == 'clinic_check':
            response = "Hold on. Let me check if you have clinics."
            send_message(sender_id, response)

        elif entity[0] == 'lab_Check':
            response = "Hold on. Let me check if you have labs."
            send_message(sender_id, response)

        if response == None:
            response = "I have no idea what you are saying!"
            send_message(sender_id, response)

    except:
        print("Get message error")
        TimeTableDatabase.ExceptionInfo()
        pass


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
