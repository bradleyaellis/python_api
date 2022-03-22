import requests

from main import VideoModel

BASE = "http://127.0.0.1:5000/"


data = [{"name":"Torpedo", "likes": 311, "views":120}, {"name":"Torpedos Go Boom", "likes": 11, "views":12},
{"name":"Torpedos Away", "likes": 31, "views": 20}]

for i in range(len(data)):
  response = requests.put(BASE + "videos/" + str(i), data[i])
  print(response.json())

input()
response = requests.get(BASE + "videos/4")
input('patching...')
patchResponse = requests.patch(BASE + 'videos/2', {})
print(patchResponse.json())

for i in range(len(data)):
  print("deleting record...")
  requests.delete(BASE + '/videos/' + str(i))
