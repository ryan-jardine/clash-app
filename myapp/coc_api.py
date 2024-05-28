import requests

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjA0ZDJhMmNmLTE2NGYtNDkyYS1iOThjLWUyMTMxYjFmNjliZiIsImlhdCI6MTcxNjg1MjY1Nywic3ViIjoiZGV2ZWxvcGVyL2FkZjBiZmZmLWFmOWYtN2Q0OC1mNjBiLTdjNWRhMjI4MmI0ZSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE1Ni41Ny4xMjIuMTI4Il0sInR5cGUiOiJjbGllbnQifV19.v6JRR9otcMrdAFk7a6UgAzrvBzldvMrNYO1Jz9mMMPqps0deC8_l9_EUi3gjRKJn8Xt-LiF9vV6xHcshhgy3fg'
}
def get_user(id):
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json()
    print(user_json)

get_user('Y9PUGGCL')
