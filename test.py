import sys

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
        self.r.set(key, value)

    def save_pipeline(self, data:dict):
        pipe = self.r.pipeline()
        #recorrer dict para sacar todos los keys y values
        for k, v in data.items():
            pipe.set(k, v)
        pipe.execute()

    def read(self, key):
        data = self.r.get(key)

        # bytes to string
        if data:
            data = data.decode('utf-8')

        # convert string to int if possible
        try:
            data = int(data)
        except:
            pass

        return data

redis = Redis(host='localhost', port=16379, db_n=1)

redis.crear_autoincremental('id')

redis.save('Bahamas', 'Nassau')
redis.save('Croatia', 'Zagreb')

print(redis.read('Bahamas'))

redis.save_pipeline(
    {
        'foo': 'bar', 
        'bing': 'queso'
    })

print(redis.read('bing'))
print(redis.read('id'))




sys.exit(99)

import requests

SERVER = "http://localhost:8000"
print(requests.get(SERVER).json())


res = requests.post(SERVER + "/chatbot", json={"msg": "bye"})
print(res.status_code)

if res.status_code == 200:
    res_data = res.json()
    print(res_data)