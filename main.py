import requests


url = "http://127.0.0.1:8000"
TOKEN = "MVIAHAbMJz8qJ0oPITsY3yO18orUMWYiM0hP7XtKVGAWDUVH4hbxNHaNqbDH"
PROPERTIES = ['color', 'count', 'shape', 'fill']
cards = []

def send_request(**kwargs):
	return requests.post(url, json = kwargs, headers={"Content-type":"application/json"}).json()

# print(send_request(hi=5,test=True))