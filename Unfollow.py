import json

f = open('followers_1.json')

data = json.load(f)

follower = []

for i in data :
    for j in i ['string_list_data']:
        follower.append(j["value"])


f = open('following.json')

data = json.load(f)

following = []

for i in data['relationships_following']:
    for j in i["string_list_data"]:
        following.append(j['value'])

goodpeople = []

for i in following:
    if i in follower:
        goodpeople.append(i)

for i in following:
    if i not in goodpeople:
        print(i)

not_following_back = []

for person in follower:
    if person not in following:
        not_following_back.append(person)

for person in not_following_back:
    print(person)