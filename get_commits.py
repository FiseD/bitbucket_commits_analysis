import requests
import json
from collections import defaultdict


ACCESS_TOKEN = 'your_access_token'


token_url = 'https://bitbucket.org/site/oauth2/authorize?client_id={}&response_type=token'
url = 'url_to_you_repp/commits?access_token={}%3D&'.format(ACCESS_TOKEN)

commits = defaultdict(dict)
page = 1
while True:
	req = requests.get(url)
	
	if req.status_code != 200:
		print('Request status is {}. Message is {}'.format(req.status_code, req.json()))
		break

	data = req.json()
	print('Page:', page)

	for i, commit in enumerate(data['values']):
		author = commit['author']
		if 'user' in author:
			user = author['user']['username']
		else:
			user = author['raw']

		date = commit['date']
		message = commit['message']

		commits[user][date] = message

		print('Commit #{}'.format(i+1))

	if 'next' in data:
		url = data['next']
		page += 1
	else:
		print('Done.')
		break

with open('data.json', 'w') as f:
	json.dump(commits, f)


