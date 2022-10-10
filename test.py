import requests

SERVER = "http://localhost:8000"
print(requests.get(SERVER).json())


res = requests.post(SERVER + "/chatbot", json={"msg": "bye"})
print(res.status_code)

if res.status_code == 200:
    res_data = res.json()
    print(res_data)