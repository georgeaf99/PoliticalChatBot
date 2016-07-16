from flask import Flask, request, redirect, session
import twilio.twiml
from twilio.rest import TwilioRestClient
import re
import jsonpickle
import sunlight
from models import Customer, Model, CFields
import messages

# The session object makes use of a secret key.
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)

@app.route('/sms/handle_sms', methods=["POST"])
def handle_sms():
    customer_phone_number = request.values["From"]
    text_message_body = request.values["Body"]

    # Get or create the customer
    customer = Model.load_from_db(Customer, customer_phone_number)

    if customer is None:
        customer = Customer.create_new({
            CFields.PHONE_NUMBER: customer_phone_number
        })
        customer.create()

    if re.match("I LIKE TURTLES", text_message_body, flags=re.IGNORECASE) is not None:
        sms.send_msg(body=messages.intro_message(), to=customer_phone_number)

    # Check to see if the message was a HELP message
    if re.match("^\s*HELP\s*$", text_message_body, flags=re.IGNORECASE) is not None:
        sms.send_msg(body=config.HELP_MESSAGE_1, to=customer_phone_number)
        sms.send_msg(body=config.HELP_MESSAGE_2, to=customer_phone_number)
        return jsonpickle.encode({"result": 0})

    # Check to see if the message was a REACHOUT message
    if re.match("^s\*REACH\s?OUT\s*$", text_message_body, flags=re.IGNORECASE) is not None:
        emails = sunlight.get_email(firstname1, lastname1, firstname2, lastname2, firstname3, lastname3)
        sms.send_msg(body=messages.reach_out(emails[0], emails[1], emails[2]), to=customer_phone_number)

    # match zipcode
    elif re.match("^\d{5}(?:[-\s]\d{4})?$", text_message_body) is not None:
        # Update the customer object
        customer['zip_code'] = text_message_body
        customer.save()

        reps=sunlight.get_reps(text_message_body)
        if len(reps) >= 3:
            sms.send_msg(body=messages.zipcode_response(reps[0],reps[1],reps[2]), to=customer_phone_number)

    return jsonpickle.encode({"result": 0})

# HELPER CLASSES #

class TwilioService():
    def __init__(self, account_sid, auth_token):
        self.twilio = TwilioRestClient(account_sid, auth_token)

    def is_connected(self):
        return len(self.twilio.accounts.list()) > 0

    def send_msg(self, to, body, from_="+18554164150"):
        sms_chunks = [body[i : i + 1600]
                for i in range(0, len(body), 1600)];

        for msg in sms_chunks:
            self.twilio.messages.create(body=msg, to=to, from_=from_)

sms = TwilioService('ACb5440a719947d5edf7d760155a39a768', 'dd9b4240a96556da1abb1e49646c73f3')

if __name__ == "__main__":
    app.run(debug=True)
