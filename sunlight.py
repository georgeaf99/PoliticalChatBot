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
    url1 = "http://openstates.org/api/v1/legislators/?first_name=" + firstname1 +"&last_name=" + lastname1 + "&apikey=" + API_KEY
    url2 = "http://openstates.org/api/v1/legislators/?first_name=" + firstname2 + "&last_name=" + lastname2 + "&apikey=" + API_KEY
    url3 = "http://openstates.org/api/v1/legislators/?first_name=" + firstname3 + "&last_name=" + lastname3 + "&apikey=" + API_KEY
    emails = []
    r1 = requests.get(url1, verify=False)
    if r1:
        json1 = r1.json()
        if json1:
            emails.append(json1[0]['email'])
        # emails += json1
    r2 = requests.get(url2, verify=False)
    if r2:
        json2 = r2.json()
        if json2:
            emails.append(json2[0]['email'])
        # emails += json2
    r3 = requests.get(url3, verify=False)
    if r3:
        json3 = r3.json()
        if json3:
            emails.append(json3[0]['email'])
        # emails += json3
    return emails

def get_recent_bill():
	url=BASE_URL+BILLS_PATH+"?history.house_passage_result__exists=true&order=history.house_passage_result_at&summary_short__exists=true&popular_title__exists=true&fields=bill_id,summary_short,popular_title"+"&apikey="+API_KEY
	r=requests.get(url)
	result = r.json()['results'][0]
	summary = result['summary_short'].split('\n\n',1)[1]
	result['summary_short'] = (summary[:500] + '..') if len(summary) > 75 else summary
	return result

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
