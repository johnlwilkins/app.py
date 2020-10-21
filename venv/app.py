'''
John Wilkins
Senior Capstone Project
FB Chatbot
10/21/2020
'''


import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_T = 'EAAFGL3tyBBgBACZAZApbsS95SZBXTIJPTZC0Dyqtf8rjtkZAxg0YhuTaFno0r5Q6lPHzOwdZCn9ZB9gpjNk3cfdaASbyAC6PwwYGzgM8rOt0jgrqJyHwMJyKRVX1Jp5w3wZAbiJpf8DFR8UVbtse0yH2mvzB2hYRXiDKfoGLZBLwUoQZDZD'
VERIFY_T = 'VERIFYTOKEN'
bot = Bot(ACCESS_T)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_s = request.args.get("hub.verify_token")
        return verify_fb_token(token_s)
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
        # take token sent by facebook and verify it matches the verify token I sent
        # if they match, allow the request, else return an error
    if token_sent == VERIFY_T:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

    # chooses a random message
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
                            "We're greatful to know you :)"]
        # return selected item to the user
    return random.choice(sample_responses)

    # uses PyMessenger to send response to user
def send_message(recipient_id, response):
        # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()





