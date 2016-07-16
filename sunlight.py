import requests

BASE_URL='https://congress.api.sunlightfoundation.com'
API_KEY='fabd1be914a141efbc8607435d2a18c0'
LEG_LOCATE_PATH='/legislators/locate'
BILLS_PATH='/bills'
OPEN_STATES_PATH="openstates.org/api/v1/legislators/"

def get_reps(zipcode):
	results = get_reps_object(zipcode)
	names=[]
	for congressmen in results:
		name=congressmen['first_name']+' '+congressmen['last_name']
		names.append(name)
	return names

def get_email(firstname1, lastname1, firstname2, lastname2, firstname3, lastname3):
    url1 = "openstates.org/api/v1/legislators/?first_name=" + firstname1 +"&last_name=" + lastname1
    url2 = "openstates.org/api/v1/legislators/?first_name=" + firstname2 + "&last_name=" + lastname2
    url3 = "openstates.org/api/v1/legislators/?first_name=" + firstname3 + "&last_name=" + lastname3
    results = r.json()['results']
    emails = []
    for congressman in results:
        emails.append(congressman['email'])
    return emails


def get_recent_bills():
	url=BASE_URL+BILLS_PATH+"?history.enacted=true&order=history.enacted_at"+"&apikey="+API_KEY
	r=requests.get(url)
	results = r.json()['results']
	return results[0:10]

def get_reps_object(zipcode):
	url=BASE_URL+LEG_LOCATE_PATH+"?zip="+zipcode+"&apikey="+API_KEY
	r=requests.get(url)
	results = r.json()['results']
	return results

def get_votes_by_congressman(zipcode):
	results = get_reps_object(zipcode)
	results = [ x['bioguide_id'] for x in results ]
	results = [ BASE_URL+"/votes?voter_ids." + x + "__exists=true"+"&fields=voter_ids"+"&apikey="+API_KEY for x in results ]
	results = [ requests.get(url).json()['results'] for url in results ]
	return [ votes[0] for votes in results ]
	# return [ [inner['voters'] for inner in result] for result in results ]
