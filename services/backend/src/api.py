import json
import uvicorn
from fastapi import FastAPI, Request
from fastapi_redis_cache import cache
from pydantic import BaseModel
from connec_redis import FastApiRedisCache, os, LOCAL_REDIS_URL
import time


# 1. Define an API object
app = FastAPI(title="backend chatbot Uniongr", description="API for chatbot", version="0.1")


from libraries.Redis import start_conection
if os.environ.get("SO") is None:
    redis = start_conection(server="localhost", port=16379)
    print("Execution in: Local")
else:
    redis = start_conection(server="redis", port=6379)
    print("Execution in: Docker")



time.sleep(2)
print("backend is ready and charging model")


# 1.1. Charge the model
from chatgui import inizia
res = inizia("hello", charge=True)

print("model charged")


# 1.2 Connect to Redis 
@app.on_event("startup")
def startup():
    print("Connecting to Redis...")
    print("Redis url: ", LOCAL_REDIS_URL)
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response]
    )


# 2. Define data type
class Msg(BaseModel):
    msg: str


class Response(BaseModel):
    message: str
    tag: str = ""


class Tags(BaseModel):
    message: list


class Intents(BaseModel):
    message: dict


class Version(BaseModel):
    version: str


# 3. Map HTTP method and path to python function
#@cache() # esta linea es para cache en redis y va despues de app.get
@app.get("/version", response_model=Version)
async def version(request: Request):
    return {"version": "1.0.0"}


# ver tags
@app.get("/tags", response_model=Tags)
async def tags(request: Request):
    model_tags = redis.read("model_tags")
    if model_tags is None:
        return {"message": []}
    else:
        tags = model_tags.get("tags")    
    print("tags: ", tags)
    return {"message": tags}


# ver intents
@app.get("/intents", response_model=Intents)
async def intents(request: Request):
    model_intents = redis.read("model_intents")
    print("intents: ", intents)
    return {"message": model_intents}


@app.get("/", response_model=Response)
async def root(request: Request):
    return {"message": "Welcome to chatbot API (backend)!"}


@app.post("/chatbot", response_model=Response)
async def get_chatbotRNA_response(inp: Msg):
    pregunta = inp.msg.upper()
    # TODO: validar palabras de censura
    # TODO: validar si la pregunta es muy larga
    # TODO: validar si la pregunta es muy corta
    # TODO: recibir datos de usuario
    # TODO: evaluar sentimiento de la pregunta

    # TODO: leer los ultimos 5 registros del historial de chat de este usuario para crear un contexto
    # TODO: evaluar si la pregunta es similar a las ultimas 5 preguntas del historial de chat de este usuario
    # TODO: evaluar si la pregunta requiere de un contexto para ser respondida
    # TODO: evaluar si las 5 ultimas preguntas del historial de chat de este usuario son similares en tags
    
    # TODO: evaluar si la pregunta requiere una respuesta de un experto
    # TODO: evaluar si la pregunta requiere de una respuesta de un experto en un tema especifico
    # TODO: revisar si el tema tiene un experto asignado
    # TODO: revisar si el tema tiene un experto asignado y si el experto esta disponible
    # TODO: revisar si el tema tiene un experto asignado y si el experto esta disponible y si el experto esta en linea
        
    # TODO: evaluar si la pregunta requiere el disparo de un evento
    # TODO: revisar si el tema tiene eventos disponibles
    
    respuesta, tag = inizia(pregunta)

    # TODO: guardar el historial de chat de este usuario en la base de datos de mongo con el formato: 
    #  {
    #       usuario: "nombre", 
    #       pregunta: "pregunta", 
    #       respuesta: "respuesta", 
    #       "date": "fecha y hora", 
    #       "sentimiento": "sentimiento"
    # }
    #  "sentimiento" es el sentimiento de la pregunta    
    
    return {
        "message": respuesta,
        "tag": tag
        }


@app.post("/train", response_model=Response)
async def train():
    # TODO: recibir las crtendiales de login
    res = inizia("hello", charge=True)
    # TODO: guardar en mongoDB una copia de los inttents.json
    # TODO: guardar en mongoDB un log de la fecha y hora de entrenamiento
    # TODO: guardar en mongoDB el log del login y la fecha y hora
    respuesta = "Sistema actualizado"
    return {"message": respuesta}


if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)


# 4. Start the API application (on command line)
# !uvicorn main:app --reload


# 5. Test the API application (on browser)
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc UI)
