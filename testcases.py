import requests as r

def login(user_id, password):
	url = "https://www.lendingclub.com/account/login.action"
	payload = {'user_id' : user_id, 'password': password}
	resp = r.post(url, params=payload)
	for each cookie in resp.cookies:
		print (cookie)
		
login('nandrea1@binghamton.edu', 'caca2tu5c')