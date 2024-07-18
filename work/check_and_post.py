import os
import pickle
import requests
import json
import urllib
import time

SW_ENDPOINT = 'https://api.foursquare.com/v2/users/self/checkins'
MD_ENDPOINT = 'https://fedibird.com/api/v1/statuses'
md_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
SW_VENUE_URL = 'https://ja.foursquare.com/v/{}'

os.chdir('/work')

with open('token', 'rb') as f:
    token_json = json.loads(f.read())
    SW_TOKEN = token_json['SW_TOKEN']
    SW_V = token_json['SW_V']
    MD_TOKEN = token_json['MD_TOKEN']

sw_params = {'oauth_token': SW_TOKEN, 'v': SW_V, 'locale': 'ja'}
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

current_time = int(time.time())

# 危ないので5件まで
for new_checkin in new_checkins[:5][::-1]:
    if new_checkin['visibility'] == 'private':
        continue
    
    check_in_created_at = new_checkin['createdAt']
    
    # 60分より前なら無視
    if current_time - check_in_created_at >= 3600:
        continue

    venue_name = new_checkin['venue']['name']
    venue_id = new_checkin['venue']['id']
    shout = ''
    if 'shout' in new_checkin:
        shout = f"({new_checkin['shout']})"
    params = {
        'access_token': MD_TOKEN,
        'status': f"I'm at {venue_name}. {shout} " + SW_VENUE_URL.format(venue_id),        
        'visibility': "unlisted"
    }

    requests.post(url=MD_ENDPOINT, data=urllib.parse.urlencode(params), headers=md_headers)

with open('checkin.pickle', 'wb') as f:
    pickle.dump(checkin_ids, f)