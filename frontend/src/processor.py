import requests
import os


IP_SERVER = "localhost" if os.environ.get("SO") is None else "backend"
SERVER = f"http://{IP_SERVER}:8000"
print("SERVER:", SERVER)


def chatbot_response(question: str):
    res = requests.post(SERVER + "/chatbot", json={"msg": question})
    if res.status_code == 200:
        res_data = res.json()
        res_data = res_data["message"]
        return res_data