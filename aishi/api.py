import requests
import tweepy as tw
import os
import json
import pymongo
import dns
from bson.objectid import ObjectId
from datetime import datetime
from time import strftime

def mmr(user, mmr_type, region):
  url='https://' + region + '.whatismymmr.com/api/v1/summoner?name=' + user.replace(' ', '+')
  headers = {'User-agent': 'Mozilla/5.0'}
  response = requests.get(url, headers = headers)
  mmr_api = response.json()
  if 'error' in mmr_api:
    return 'error'
  else:
    return mmr_api[mmr_type]['avg']

def twt(action, user):
  auth = tw.OAuthHandler(os.environ.get("CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
  auth.set_access_token(os.environ.get("ACCESS_TOKEN"), os.environ.get("ACCESS_TOKEN_SECRET"))
  api = tw.API(auth, wait_on_rate_limit=True)
  status_list = api.user_timeline(user, count=1)
  status = status_list[0]
  json_str = json.loads(json.dumps(status._json))
  og = json_str['text']
  if action == 'raid':
    split = og.split(" ")
    battleID = split[(split.index(':Battle')-1)]
    raidName = split[len(split)-1]
    if is_number(split[split.index(raidName)-1]) == False:
      raidName = split[split.index(raidName)-1] + ' ' + raidName
    raidName = raidName.split('\n')[0]
    return battleID, raidName, og
  elif action == 'egg':
    checker = '#NeweggShuffle'
    if checker in og:
      tweettime = json_str['created_at'].split(" ")[1:]
      tweettime.pop(3)
      timestamp1 = tweettime[0]
      for i in range(1, len(tweettime)):
        timestamp1+=" " + tweettime[i]
      timestamp2 = strftime("%b %d %H:%M:%S %Y")

      t1 = datetime.strptime(timestamp1, "%b %d %H:%M:%S %Y")
      t2 = datetime.strptime(timestamp2, "%b %d %H:%M:%S %Y")

      difference = t2 - t1
      if difference.total_seconds() < 10:
        return og

def is_number(string):
  try:
    float(string)
    return True
  except ValueError:
    return False

def data(database, action, userid = '', data = ''):
  # MONGODB
  client = pymongo.MongoClient(str(os.environ.get("MONGODB")))
  # The ismaster command is cheap and does not require auth.
  client.admin.command('ismaster')
  db = client.aishi
  if database == 'profile':
    collection = db['aishicollect']
    try:
      if action == 'create' or action == 'delete':
        if action == 'create':
          info = {"_id": str(userid), 'labels': data}
          try:
            info["labels"].update(collection.find_one({"_id": str(userid)})["labels"])
          except:
            print("error")
          collection.update_one({"_id": info["_id"]}, {"$set": {"labels": info["labels"]}}, upsert = True)   
        elif action == 'delete':
          info = collection.find_one({"_id": str(userid)})
          info['labels'].pop(data)
          collection.update_one({"_id": info["_id"]}, {"$set": {"labels": info["labels"]}}, upsert = True)
      elif action == 'deleteall':
        collection.remove({"_id": str(userid)})
      elif action == 'read':
        info = collection.find_one({"_id": str(userid)})
        if info is None:
          return "error"
        else:
          return info
    except:
        print("error")
        return "error"
  elif database == 'egg':
    collection = db['eggsub']
    try:
      if action == 'create':
        info = collection.find_one({"_id": str(userid)})
        if info is None:
          collection.insert({"_id": str(userid)})
        else:
          return "done"
      elif action == 'deleteall':
        collection.remove({"_id": str(userid)})
      elif action == 'read':
        memberids = []
        for document in collection.find():
          memberids.append(document['_id'])
        return memberids
    except:
      print("error")
      return "error"

def transfer():
  # MONGODB
  client = pymongo.MongoClient(str(os.environ.get("MONGODB")))
  # The ismaster command is cheap and does not require auth.
  client.admin.command('ismaster')
  db = client.aishi
  collection = db['aishicollect']
  try:
    #info = {"_id": str(userid), 'labels': data}
    with open('data.json', 'r') as fp:
      info = json.load(fp)
      for i in list(info):
        collection.update_one({"_id": i}, {"$set": {"labels": info[i]['games']}}, upsert = True)
  except:
    return 'error'

def riot(user, gametype, region = 'na'):
  try:
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
  except:
    return 'unableToRetrieve'
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

