import requests
url = "https://postman-echo.com/post"

def send_request(**kwargs):
	return requests.post(url, json = kwargs, headers={"Content-type":"application/json"}).json()

print(send_request(hi=5,test=True))