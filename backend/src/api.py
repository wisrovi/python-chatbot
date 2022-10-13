import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

from chatgui import inizia

res = inizia("hello", charge=True)


# 1. Define an API object
app = FastAPI()


# 2. Define data type
class Msg(BaseModel):
    msg: str


class Response(BaseModel):
    message: str


# 3. Map HTTP method and path to python function
@app.get("/", response_model=Response)
async def root(request: Request):
    return {"message": "Welcome to chatbot API (backend)!"}


@app.post("/chatbot", response_model=Response)
async def function_demo_post(inp: Msg):
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
    
    respuesta = inizia(pregunta)

    # TODO: guardar el historial de chat de este usuario en la base de datos de mongo con el formato: 
    #  {
    #       usuario: "nombre", 
    #       pregunta: "pregunta", 
    #       respuesta: "respuesta", 
    #       "date": "fecha y hora", 
    #       "sentimiento": "sentimiento"
    # }
    #  "sentimiento" es el sentimiento de la pregunta    
    
    return {"message": respuesta}


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
    uvicorn.run(app, host="0.0.0.0", port=8000)


# 4. Start the API application (on command line)
# !uvicorn main:app --reload


# 5. Test the API application (on browser)
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc UI)
