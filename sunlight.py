import requests

BASE_URL='https://congress.api.sunlightfoundation.com'
API_KEY='fabd1be914a141efbc8607435d2a18c0'
LEG_LOCATE_PATH='/legislators/locate'
BILLS_PATH='/bills'

def get_reps(zipcode):
	url=BASE_URL+LEG_LOCATE_PATH+"?zip="+zipcode+"&apikey="+API_KEY
	r=requests.get(url)
	results = r.json()['results']
	names=[]
	for congressmen in results:
		name=congressmen['first_name']+' '+congressmen['last_name']
		names.append(name)
	return names

def get_email(firstname1, lastname1, firstname2, lastname2, firstname3, lastname3):
    url1 = "openstates.org/api/v1/legislators/?first_name=" + firstname1 +"&last_name=" + lastname1
    url2 = "openstates.org/api/v1/legislators/?first_name=" + firstname2 + "&last_name=" + lastname2
    url3 = "openstates.org/api/v1/legislators/?first_name=" + firstname3 + "&last_name=" + lastname3
    emails = []
    r1 = requests.get(url1)
    emails.append(r1.json()['email']
    r2 = requests.get(url2)
    emails.append(r2.json()['email']
    r3 = requests.get(url3)
    emails.append(r3.json()['email']
    return emails

def get_recent_bills():
	url=BASE_URL+BILLS_PATH+"?history.enacted=true&order=history.enacted_at"+"&apikey="+API_KEY
	r=requests.get(url)
	results = r.json()['results']
	return results[0:10]

