import requests
import config
import json

class Site:
	def __init__(self, id, lookupcode, latitude, longitude):
		self.id = id
		self.lookupcode = lookupcode
		self.latitude = latitude
		self.longitude = longitude

class Device:
	def __init__(self, id, model, address, lookupcode, host_name):
		self.id = id
		self.model = model
		self.address = address
		self.lookupcode = lookupcode
		self.host_name = host_name

def fetch_sis_api(path, params = {}, env = config.env):
	url = "https://anss-sis.scsn.org/"+env+"/api/v1/"+path
	headers = {'Authorization': 'Bearer '+config.api_key,}
	params['ownercode'] = config.ownercode
	if params.get('page[size]') is None:
		params['page[size]'] = config.page_size
	#print(params)
	r = requests.get(url, headers = headers, params=params)
	#print(r.url)
	res = r.json()

	return(res)
