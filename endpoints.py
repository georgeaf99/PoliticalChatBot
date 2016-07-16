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
        sms.send_msg(body="Welcome to PolitiHack! Text us 'EXAMPLES' for a list of commands.", to=customer_phone_number)

        customer = Customer.create_new({
            CFields.PHONE_NUMBER: customer_phone_number
        })
        customer.create()

    # Check to see if the customer was prompted
    if customer['prompted']:
        customer['prompted'] = False
        customer.save()

        if re.match("^\s*YES\s*$", text_message_body, flags=re.IGNORECASE) is not None:
            # TODO: Save votes
            sms.send_msg(body=messages.bill_vote_response(), to=customer_phone_number)
        elif re.match("^\s*NO\s*$", text_message_body, flags=re.IGNORECASE) is not None:
            # TODO: Save votes
            sms.send_msg(body=messages.bill_vote_response(), to=customer_phone_number)
        elif re.match("^\s*MORE INFORMATION\s*$", text_message_body, flags=re.IGNORECASE) is not None:
            # TODO: Return whole bill summary
            pass

    if re.match("^\s*EXAMPLE(S)?\s*$", text_message_body, flags=re.IGNORECASE) is not None:
        sms.send_msg(body="Commands: your zip code, GET BILLS, REACH OUT, STATS", to=customer_phone_number)
    # Check to see if the message was a REACHOUT message
    elif re.match("^\s*REACH\s?OUT\s*$", text_message_body, flags=re.IGNORECASE) is not None:
        reps = [rep.split(' ') for rep in sunlight.get_reps(customer[CFields.ZIP_CODE])]

        emails = sunlight.get_email(reps[0][0], reps[0][1], reps[1][0], reps[1][1], reps[2][0], reps[2][1])

        if emails:
            sms.send_msg(body=messages.reach_out(emails[0], emails[1], emails[2]), to=customer_phone_number)
        else:
            sms.send_msg(body="Your congressmen do not have contact information!", to=customer_phone_number)
    elif re.match("\s*GET\s?BILLS\s*$", text_message_body, flags=re.IGNORECASE) is not None:
        bill = sunlight.get_recent_bill()

        # save the customers state
        customer['prompted'] = True
        customer['bill_id'] = bill['bill_id']
        customer.save()

        # Display the bills
        sms.send_msg(body=messages.bill(bill['popular_title'], bill['summary_short']), to=customer_phone_number)

        # Follow up on the bill
        sms.send_msg(body=messages.bill_followup(), to=customer_phone_number)
    # match zipcode
    elif re.match("^\d{5}(?:[-\s]\d{4})?$", text_message_body) is not None:
        # Update the customer object
        customer['zip_code'] = text_message_body
        customer.save()

        reps=sunlight.get_reps(text_message_body)
        if len(reps) >= 3:
            sms.send_msg(body=messages.zipcode_response(reps[0],reps[1],reps[2]), to=customer_phone_number)

    elif re.match("^\s*STATS\s*$", text_message_body) is not None:
        # TODO: add implementation for stats.
        pass
    else:
        if re.match("^\s*YES\s*$", text_message_body, flags=re.IGNORECASE) is None and \
                re.match("^\s*NO\s*$", text_message_body, flags=re.IGNORECASE) is None:
            # TODO: Save votes
            sms.send_msg(body="Commands: your zip code, GET BILLS, REACH OUT, STATS", to=customer_phone_number)

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
