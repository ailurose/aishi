import requests
import tweepy as tw
import os
import json
import pymongo
import dns
from bson.objectid import ObjectId
from datetime import datetime
from time import strftime
import time

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
  try:
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
  except tw.error.TweepError:
    time.sleep(10*60)

def is_number(string):
  try:
    float(string)
    return True
  except ValueError:
    return False

#original data method
'''
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
              info[i]['games'].pop(data) 
    with open('data.json', 'w') as fp:
      json.dump(info, fp)
  if action == 'deleteall':
    with open('data.json', 'r') as fp:
      info = json.load(fp)
      for i in list(info):
        if str(userid)==i:
          info[i]['games'].clear()
    with open('data.json', 'w') as fp:
      json.dump(info, fp)
'''

#new data method
def data(database, action, userid = '', data = ''):
  # MONGODB
  client = pymongo.MongoClient(str(os.environ.get("MONGODB")))
  # The ismaster command is cheap and does not require auth.
  client.admin.command('ismaster')
  db = client.aishi
  database_list = 'profile, remind, special'
  if database in database_list:
    if database == 'profile':
      collection = db['aishicollect']
    elif database == 'remind':
      collection = db['remind']
      months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    elif database == 'special':
      collection = db['specialmsgs']
    keylabels = {'profile': 'labels', 'remind': 'reminders'}
    try:
      if action in 'create, delete':
        if action == 'create':
          if database == 'profile':
            info = {"_id": str(userid), 'labels': data}
          elif database == 'remind':
            try:
              timeremind = data[1]
              timesplitter = timeremind.split(' ')
              datesplitter = timesplitter[0].split('-')
              datetime1 = months[int(datesplitter[1])-1] + ' ' + datesplitter[2] + ' ' + timesplitter[1] + ' ' + datesplitter[0]
              timeremindformat = datetime.strptime(datetime1, "%b %d %H:%M:%S %Y")
              data[1] = timeremindformat
              datadict = {data[0]: data[1]}
              info = {"_id": str(userid), 'reminders': datadict}
            except:
              print("formaterror")
              return "formaterror"
          elif database == 'special':
            info = {"_id": str(userid), 'special': data}
          try:
            info[keylabels[database]].update(collection.find_one({"_id": str(userid)})[keylabels[database]])
          except:
            print("previous entry non-existant")
          collection.update_one({"_id": info["_id"]}, {"$set": {keylabels[database]: info[keylabels[database]]}}, upsert = True)   
        elif action == 'delete':
          info = collection.find_one({"_id": str(userid)})
          info[keylabels[database]].pop(data)
          collection.update_one({"_id": info["_id"]}, {"$set": {keylabels[database]: info[keylabels[database]]}}, upsert = True)
      elif action == 'deleteall':
        collection.remove({"_id": str(userid)})
      elif action == 'read':
        info = collection.find_one({"_id": str(userid)})
        if info is None:
          return "error"
        else:
          return info
      elif action == 'readall' and database == 'remind':
        remindingMembers = {'memberids':[], 'reminders':[]}
        for document in collection.find():
          reminders = []
          for reminder in document['reminders']:
            remindtime = document['reminders'][reminder]
            timestamp2 = strftime("%b %d %H:%M:%S %Y")
            t2 = datetime.strptime(timestamp2, "%b %d %H:%M:%S %Y")
            difference = remindtime - t2
            if difference.total_seconds() < 10 and difference.total_seconds() > 0:
              reminders.append(reminder)
          if len(reminders) > 0:
            remindingMembers['memberids'] = remindingMembers['memberids'].append(document['_id'])
            remindingMembers['reminders'] = remindingMembers['reminders'].append(reminders)
        if len(remindingMembers['memberids']) == 0:
          return "error", t2
        else:
          return info, t2
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
  elif database == 'feedback':
    collection = db['feedback']
    try:
      if action == 'create':
          entrytime = strftime("%b %d %H:%M:%S %Y")
          et = datetime.strptime(entrytime, "%b %d %H:%M:%S %Y")
          info = {"_id": str(userid), 'feedback': {entrytime: data}}
          try:
            fbdict = collection.find_one({"_id": str(userid)})["feedback"]
            for i in fbdict.keys():
              lastfb = datetime.strptime(i, "%b %d %H:%M:%S %Y")
              difference = et - lastfb
              if difference.total_seconds() < 300:
                print(difference.total_seconds())
                return "timeout"
            info["feedback"].update(fbdict)
          except:
            print("previous entry non-existant")
          collection.update_one({"_id": str(userid)}, {"$set": {"feedback": info['feedback']}}, upsert = True)
    except:
      print("error")
      return "error"
  '''  
  elif database == 'remind':
    collection = db['remind']
    try:
      if action == 'create' or 'delete':
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        try:
          timeremind = data[0]
          timesplitter = timeremind.split(' ')
          datesplitter = timesplitter[0].split('-')
          datetime1 = months[int(datesplitter[1])] + ' ' + datesplitter[2] + ' ' + timesplitter[1] + ' ' + datesplitter[0]
          timeremindformat = datetime.strptime(datetime1, "%b %d %H:%M:%S %Y")
          data[0] = timeremindformat
          info = {"_id": str(userid), 'reminders': data}
          if action == 'create':
            try:
              info["labels"].update(collection.find_one({"_id": str(userid)})["reminders"])
            except:
              print("previous entry non-existant")
            collection.update_one({"_id": info["_id"]}, {"$set": {"reminders": info["reminders"]}}, upsert = True)
          elif action == 'delete':
            info = collection.find_one({"_id": str(userid)})
            info['reminders'].pop(data)
            collection.update_one({"_id": info["_id"]}, {"$set": {"reminders": info["reminders"]}}, upsert = True)
        except:
          print("formaterror")
          return "formaterror"
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
    '''      

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

