def intro_message():
    return "Welcome to PolitiHack, a simple service to keep you involved in democracy. Please reply with your zipcode to begin."

def zipcode_response(congressman, senator1, senator2):
    return "Your representatives are: \n - {} \n - {} \n - {}".format(congressman, senator1, senator2)

def bill(title, summary):
    return "Bill Update: {}\n {}".format(title, summary)

def bill_followup():
    return "Respond with 'Yes' or 'No'

def bill_vote_response():
    return "Thanks for your feedback. If you feel strongly about this issue and would like to reach out directly to your representatives, reply 'Reach Out'"

def reach_out(email1, email2, email3):
    return "Great! Here are your representatives emails: {} \n {} \n {}".format(email1, email2, email3)

def election_update():
    return "An election is upcoming in your area. Here is how your opinions align with the candidates:"

def canidate_analytics(agree_percent):
    "You have agreed on {} of bills presented to you with your representatives".format(agree_percent)

def no_email():
    return "Your congressmen do not have contact information."
