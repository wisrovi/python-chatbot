import requests
import os


IP_SERVER_CHAT = "localhost" if os.environ.get("SO") is None else "backend"
SERVER_CHAT = f"http://{IP_SERVER_CHAT}:8000"
print("SERVER_CHAT:", SERVER_CHAT)

IP_SERVER_RNA = "localhost" if os.environ.get("SO") is None else "training"
SERVER_RNA = f"http://{IP_SERVER_RNA}:8887"
print("SERVER_RNA:", SERVER_RNA)


def chatbot_response(question: str):
    res = requests.post(SERVER_CHAT + "/chatbot", json={"msg": question})
    if res.status_code == 200:
        res_data = res.json()
        res_data = res_data["message"]
        return res_data


def informar_nuevo_modelo(question: str = "credenciales login"):
    res = requests.post(SERVER_CHAT + "/train", json={"msg": question})
    if res.status_code == 200:
        res_data = res.json()
        res_data = res_data["message"]
        return res_data


def solicitar_entrenamiento():
    question = "entrenar"
    mensaje = "Error"
    status = 404
    res = requests.post(SERVER_RNA + "/RNA", json={"msg": question})
    if res.status_code == 200:
        res_data = res.json()
        mensaje = res_data["response"]
        status = res_data["status"]
    return mensaje, status