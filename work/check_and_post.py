import os
import pickle
import requests
import json
import urllib

SW_ENDPOINT = 'https://api.foursquare.com/v2/users/self/checkins'
MD_ENDPOINT = 'https://fedibird.com/api/v1/statuses'
md_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
SW_CHECKIN_URL = 'https://www.swarmapp.com/opierio/checkin/{}'

os.chdir('/work')

with open('token', 'rb') as f:
    token_json = json.loads(f.read())
    SW_TOKEN = token_json['SW_TOKEN']
    SW_V = token_json['SW_V']
    MD_TOKEN = token_json['MD_TOKEN']

sw_params = {'oauth_token': SW_TOKEN, 'v': SW_V}
sw_resp = requests.get(SW_ENDPOINT, params=sw_params)

resp_json = sw_resp.json()['response']
checkins = resp_json['checkins']['items']
checkin_ids = [item['id'] for item in checkins]

with open('checkin.pickle', 'rb') as f:
    stored_checkin_ids = pickle.load(f)

new_checkin_id = []

for checkin_id in checkin_ids:
    if not checkin_id in stored_checkin_ids:
        new_checkin_id.append(checkin_id)

new_checkins = [item for item in checkins if item['id'] in new_checkin_id]

for new_checkin in new_checkins[:3]:
    venue_name = new_checkin['venue']['name']
    checkin_id = new_checkin['id']
    shout = new_checkin['shout']
    params = {
        'access_token': MD_TOKEN,
        'status': f"I'm at {venue_name}. ({shout}) " + SW_CHECKIN_URL.format(checkin_id),
        'visibilty': 'unlisted'
    }

    requests.post(url=MD_ENDPOINT, data=urllib.parse.urlencode(params), headers=md_headers)

with open('checkin.pickle', 'wb') as f:
    pickle.dump(checkin_ids, f)