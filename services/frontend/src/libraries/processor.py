import requests
import os


"""
Funciones para tratar con el backend
"""
IP_SERVER_CHAT = "localhost" if os.environ.get("SO") is None else "backend"
SERVER_BACKEND_CHAT = f"http://{IP_SERVER_CHAT}:8000"
print("SERVER_BACKEND_CHAT:", SERVER_BACKEND_CHAT)


def chatbot_response(question: str):
    response = tag = ""
    res = requests.post(SERVER_BACKEND_CHAT + "/chatbot", json={"msg": question})
    if res.status_code == 200:
        res_data = res.json()
        response = res_data["message"]
        tag = res_data["tag"]
        return response, tag


def informar_nuevo_modelo(question: str = "credenciales login"):
    res = requests.post(SERVER_BACKEND_CHAT + "/train", json={"msg": question})
    if res.status_code == 200:
        res_data = res.json()
        res_data = res_data["message"]
        return res_data


def get_version_backend():
    res = requests.get(SERVER_BACKEND_CHAT + "/version")
    if res.status_code == 200:
        res_data = res.json()
        return res_data["version"]
    return "Error"


def get_tags():
    res = requests.get(SERVER_BACKEND_CHAT + "/tags")
    if res.status_code == 200:
        res_data = res.json()
        return res_data["message"]
    return "Error"


def get_intents():
    res = requests.get(SERVER_BACKEND_CHAT + "/intents")
    if res.status_code == 200:
        res_data = res.json()
        return res_data["message"]
    return "Error"


"""
    Funciones para tratar con el training
"""
IP_SERVER_RNA = "localhost" if os.environ.get("SO") is None else "training"
SERVER_RNA = f"http://{IP_SERVER_RNA}:8887"
print("SERVER_RNA:", SERVER_RNA)

def get_version_training():
    res = requests.get(SERVER_RNA + "/version")
    if res.status_code == 200:
        res_data = res.json()
        return res_data["version"]
    return "Error"


def solicitar_entrenamiento():
    question = "entrenar"
    mensaje = "Error"
    status = 404
    res_data = dict()

    res = requests.post(SERVER_RNA + "/RNA", json={"msg": question})
    if res.status_code == 200:
        res_data = res.json()
        mensaje = res_data["response"]
        status = res_data["status"]
    return list((mensaje, status)), res_data