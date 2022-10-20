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


def start_conection(server, port):
    redis = Redis(host=server, port=port, db_n=1)
    return redis