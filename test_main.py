import requests
# url = "https://postman-echo.com/post"
url = ""
token = ""
gameId = 0


def test_register():
	nick = "vanka"
	pswd = 242424
	response = send_request("/user/login", nickname=nick, password=pswd)
	check_response(response, success=True, nickname=nick, accessToken=None, exception=None)
	global token
	token = response["accessToken"]

def test_create_game():
	response = send_request("/set/room/create", accessToken=token)
	check_response(response, success=True, error=None, gameId=None)
	global gameId
	gameId = response["gameId"]

# test_register()
# test_create_game()


