import json

import requests

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjA0ZDJhMmNmLTE2NGYtNDkyYS1iOThjLWUyMTMxYjFmNjliZiIsImlhdCI6MTcxNjg1MjY1Nywic3ViIjoiZGV2ZWxvcGVyL2FkZjBiZmZmLWFmOWYtN2Q0OC1mNjBiLTdjNWRhMjI4MmI0ZSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE1Ni41Ny4xMjIuMTI4Il0sInR5cGUiOiJjbGllbnQifV19.v6JRR9otcMrdAFk7a6UgAzrvBzldvMrNYO1Jz9mMMPqps0deC8_l9_EUi3gjRKJn8Xt-LiF9vV6xHcshhgy3fg'
}


def get_user(id):
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    if response.status_code == 200:
        user_json = response.json()
    else:
        user_json = "User does not exist"
    return user_json


user = get_user('Y9PUGGCL')


def get_gp():
    response = requests.get('https://api.clashofclans.com/v1/goldpass/seasons/current', headers=headers)
    gp_json = response.json()
    return gp_json


# Store Relevant user information in an Object
class PlayerInfo:
    def __init__(self, user_json):
        self.name = user_json['name']
        self.tag = user_json['tag']
        self.townHall = user_json['townHallLevel']
        self.exp = user_json['expLevel']
        self.trophies = user_json['trophies']
        self.bestTrophies = user_json['bestTrophies']
        self.warStars = user_json['warStars']


class GameInfo:
    def __init__(self, gp_json):
        self.gpStart = gp_json['startTime']
        self.gpEnd = gp_json['endTime']


gameInfo = GameInfo(get_gp())
print(gameInfo.gpStart)

player = PlayerInfo(user)
print(player.name)
