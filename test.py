import json


class Redis(object):
    import redis
    def __init__(self, host, port, db_n=0):
        self.host = host
        self.port = port
        self.db_n = db_n     

        self.__connect()   

    def __connect(self):
        self.r = self.redis.Redis(host=self.host, port=self.port, db=self.db_n)

    def crear_autoincremental(self, key):
        return self.r.incr(key)

    def save(self, key, value):
        if isinstance(value, dict):
            value = json.dumps(value)
        
        self.r.set(key, value)

    def save_pipeline(self, data:dict):
        pipe = self.r.pipeline()
        #recorrer dict para sacar todos los keys y values
        for k, v in data.items():
            pipe.set(k, v)
        pipe.execute()

    def read(self, key):
        try:
            data = self.r.get(key)
        except Exception as e:
            return None

        # convertir a dict si es posible
        try:
            data = json.loads(data)
        except:
            pass

        # bytes to string
        try:
            data = data.decode('utf-8')
        except:
            pass

        # convert string to int if possible
        try:
            data = int(data)
        except:
            pass

        return data

    def read_dict(self, key):
        return self.r.hgetall(key)

redis = Redis(host='localhost', port=16379, db_n=1)

redis.crear_autoincremental('id')

redis.save('Bahamas', 'Nassau')
redis.save('Croatia', 'Zagreb')
redis.save('comida', {
    "fruta": "manzana",
    "verdura": "lechuga",
    "carne": "pollo"
})

print(redis.read('Bahamas'))

redis.save_pipeline(
    {
        'foo': 'bar', 
        'bing': 'queso'
    })

print(redis.read('bing'))
print(redis.read('id'))
print(redis.read('comida'))



d = {
    "intents": [
        {
            "tag": "colaboradores",
            "patterns": [
                "donde puedo consultar informacion de los colaboradores",
                "donde puedo consultar la informacion como trabajador",
                "colaboradores",
                "trabajadores",
                "informacion empleados",
                "colaborador  "
            ],
            "responses": [
                "la puedes consultar en el siguiente link",
                "puedes consultar las siguientes inquietudes en el siguiente link",
                "en el siguiente link te daremos una informacion mucho mas detallada"
            ],
            "context": []
        },
        {
            "tag": "contactenos",
            "patterns": [
                "Adiós",
                "Hasta luego",
                "Adiós",
                "Encantado de charlar contigo, adiós",
                "Hasta la próxima"
            ],
            "responses": [
                "Hasta luego, gracias por visitarnos",
                "Que tengas un buen día",
                "¡Adiós! Vuelve pronto"
            ],
            "context": []
        },
        {
            "tag": "goodbye",
            "patterns": [
                "Adiós",
                "Hasta luego",
                "Adiós",
                "Encantado de charlar contigo, adiós",
                "Hasta la próxima"
            ],
            "responses": [
                "Hasta luego, gracias por visitarnos",
                "Que tengas un buen día",
                "¡Adiós! Vuelve pronto"
            ],
            "context": []
        },
        {
            "tag": "gracias",
            "patterns": [
                "Gracias",
                "Eso es útil",
                "Impresionante, gracias",
                "Gracias por ayudarme"
            ],
            "responses": [
                "¡Feliz de ayudar!",
                "¡Cualquier momento!",
                "Es un placer"
            ],
            "context": []
        },
        {
            "tag": "habeas_data",
            "patterns": [
                "Adiós",
                "Hasta luego",
                "Adiós",
                "Encantado de charlar contigo, adiós",
                "Hasta la próxima"
            ],
            "responses": [
                "Hasta luego, gracias por visitarnos",
                "Que tengas un buen día",
                "¡Adiós! Vuelve pronto"
            ],
            "context": []
        },
        {
            "tag": "noanswer",
            "patterns": [],
            "responses": [
                "Lo siento, no puedo entenderte"
            ],
            "context": []
        },
        {
            "tag": "saludo",
            "patterns": [
                "Hola",
                "Cómo estás?",
                "¿Hay alguien ahí?",
                "Hola",
                "Hey",
                "Buenos días"
            ],
            "responses": [
                "Hola, gracias por visitar",
                "Qué bueno verte de nuevo",
                "Hola, ¿cómo puedo ayudar?"
            ],
            "context": []
        },
        {
            "tag": "t_e.csv",
            "patterns": [],
            "responses": [],
            "context": []
        }
    ]
}

redis.save('intents', d)

d = redis.read('intents')
print(d)


import sys
sys.exit(99)

import requests

SERVER = "http://localhost:8000"
print(requests.get(SERVER).json())


res = requests.post(SERVER + "/chatbot", json={"msg": "bye"})
print(res.status_code)

if res.status_code == 200:
    res_data = res.json()
    print(res_data)