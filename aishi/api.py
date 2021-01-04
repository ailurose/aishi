import requests
import tweepy as tw
import os
import json

def mmr(user, mmr_type, region):
  url='https://' + region + '.whatismymmr.com/api/v1/summoner?name=' + user.replace(' ', '+')
  headers = {'User-agent': 'Mozilla/5.0'}
  response = requests.get(url, headers = headers)
  mmr_api = response.json()
  if 'error' in mmr_api:
    return 'error'
  else:
    return mmr_api[mmr_type]['avg']

def twt(user):
  auth = tw.OAuthHandler(os.environ.get("CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
  auth.set_access_token(os.environ.get("ACCESS_TOKEN"), os.environ.get("ACCESS_TOKEN_SECRET"))
  api = tw.API(auth, wait_on_rate_limit=True)
  status_list = api.user_timeline(user, count=1)
  status = status_list[0]
  json_str = json.loads(json.dumps(status._json))
  og = json_str['text']
  split = og.split(" ")
  battleID = split[(split.index(':Battle')-1)]
  raidName = split[len(split)-1]
  if is_number(split[split.index(raidName)-1]) == False:
    raidName = split[split.index(raidName)-1] + ' ' + raidName
  raidName = raidName.split('\n')[0]
  return battleID, raidName, og,

def is_number(string):
  try:
    float(string)
    return True
  except ValueError:
    return False

def data(action, userid = '', data = ''):
  if action == 'create':
    try:
      with open('data.json', 'r') as fp:
        info = json.load(fp)
        for i in list(info):
          if str(userid)==i:
            if list(data.keys())[0] in list(info[i]['games']):
              info[i]['games'][list(data.keys())[0]] = data[list(data.keys())[0]]
            else:
              info[i]['games'].update(data)
            with open('data.json', 'w') as fp:
              json.dump(info, fp)
            return
        with open('data.json', 'w') as fp:
          dict = {str(userid): {'games': data}}
          info.update(dict)
          json.dump(info,fp)
    except:
      return 'error'
  if action == 'read':
    with open('data.json', 'r') as fp:
      info = json.load(fp)
      for i in list(info):
        if str(userid) == i:
          return info[i]
      return 'error'
  if action == 'delete':
    with open('data.json', 'r') as fp:
      info = json.load(fp)
      for i in list(info):
        if str(userid)==i:
          for game in list(info[i]['games']):
            if data == game:
              print(info)
              info[i]['games'].pop(data) 
              print(info)
    with open('data.json', 'w') as fp:
      json.dump(info, fp)
  if action == 'deleteall':
    with open('data.json', 'r') as fp:
      info = json.load(fp)
      for i in list(info):
        if str(userid)==i:
          print(info)
          info[i]['games'].clear()
          print(info)
    with open('data.json', 'w') as fp:
      json.dump(info, fp)
          
  '''
  JSON_BIN
  secret_key = str(os.environ.get("JSON_SECRET"))
  if action == 'create':
    url = 'https://api.jsonbin.io/b'
    headers = {
      'Content-Type': 'application/json',
      'secret-key': '$2b$10$PzNQERQktkdpFOl49BFRPurKRVD0SYSi94UarTHm6nyT.3M7RDr5y',
      'name': str(userid),
      'collection-id': '5fe950276c160b7b70da508f'
    }
    response = requests.post(url, json=data, headers=headers)
  elif action == 'read':
    url = 'https://api.jsonbin.io/e/collection/' + os.environ.get("JSON_COLLECTION") + '/all-bins'
    headers = {'secret-key': '$2b$10$PzNQERQktkdpFOl49BFRPurKRVD0SYSi94UarTHm6nyT.3M7RDr5y'}
    response = requests.get(url, headers=headers)
    print(response)
    json_str = json.loads(json.dumps(response.json()))
    print(json_str)
    try:
      records = json_str['records']
      user = ''
      for r in records:
        url = 'https://api.jsonbin.io/b/' + r['id']
        response = requests.get(url, headers=headers)
        json_str = json.loads(json.dumps(response.json()))
        print(json_str)
        print(str(json_str['userid']) + 'vs.' + str(userid))
        if json_str['userid'] == userid:
          user = json_str['userid']
          print(user)
    except KeyError:
      return 'error'
  '''
  '''
  # MONGODB
  #import pymongo
  #from pymongo.errors import ConnectionFailure
  client = pymongo.MongoClient(str(os.environ.get("MONGODB")), connect = False)
  try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    db = client["aishi"]
    collection = db["aishicollect"]

    if action == 'create':
      myquery = {"_id" : userid}
      if (collection.count_documents(myquery) == 0):
        post = {"_id" : userid, game[0]: game[1]}
        collection.insert_one(post, connect = False)
      else:
        collection.update_one({"_id": userid}, {"$set": {game[0], game[1]}})
    elif action == 'read':
      myquery = {"_id" : userid}
      try:
        cursor = collection.find(myquery)
        print(cursor)
      except TypeError:
        return "error"
  except ConnectionFailure:
    print("Server not available")
    return "error"
  '''


def riot(user, gametype, region = 'na'):
  user1 = user.split(' ')
  ulink = user1[0]
  if len(user) > 1:
    for u in range(len(user1)-1):
      ulink = ulink + '%20' + user1[u+1]
  url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + ulink + '?api_key=' + str(os.environ.get('RIOT_KEY'))
  response = requests.get(url)
  summoner_api = response.json()
  summoner = summoner_api['id']
  url = 'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + summoner + '?api_key=' + str(os.environ.get('RIOT_KEY'))
  response = requests.get(url)
  summoner_api = response.json()
  try:
    players = summoner_api['participants']
    teams = {'team1':[], 'team2':[]}
    num = 1
    for player in players:
      p = [player['summonerName'], mmr(player['summonerName'], gametype, region)]
      if num <= 5:
        teams['team1'].append(p)
      else:
        teams['team2'].append(p)

      if player['summonerName'].lower()==user:
        if num<=5:
          teams['playerTeam'] = 'team1'
        else:
          teams['playerTeam'] = 'team2'
      num+=1
    return teams
  except KeyError:
    return 'error'

