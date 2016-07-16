def intro_message():
    return "Welcome to PolitiHack, a simple service to keep you involved in democracy. Please reply with your zipcode to begin."

def zipcode_response(congressman, senator1, senator2):
    return "Your representatives are: \n {} \n {} \n {}".format(congressman, senator1, senator2)

def bill(title, summary):
    return "Bill Update: {}\n {}".format(title, summary)

def bill_followup():
    return "Respond with 'Yes', 'No', or 'More Information'"

def bill_vote_response():
    return "Thanks for your feedback. If you feel strongly about this issue and would like to reach out directly to your representatives, reply 'Reach Out'"

def reach_out():
    return "Great! You can either respond directly to this message, or respond with 'Email' to get their emails. Otherwise type 'Cancel'"

def reach_out_response():
    return "Thanks for your feedback. We'll be sure to pass it along"

def election_update():
    return "An election is upcoming in your area. Here is how your opinions align with the candidates:"

def canidate_analytics(candidate_name, agree_percent):
    "{} You have agreed on {} of bills presented to you".format(candidate_name, agree_percent)
