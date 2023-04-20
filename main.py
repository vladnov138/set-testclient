import requests


url = "https://postman-echo.com/post"
TOKEN = ""
PROPERTIES = ['color', 'count', 'shape', 'fill']
cards = []

def send_request(**kwargs):
	return requests.post(url, json = kwargs, headers={"Content-type":"application/json"}).json()

print(send_request(hi=5,test=True))