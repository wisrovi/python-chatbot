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
    respuesta = inizia(pregunta)
    return {"message": respuesta}


@app.post("/train", response_model=Response)
async def train():
    res = inizia("hello", charge=True)
    respuesta = "Sistema actualizado"
    return {"message": respuesta}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# 4. Start the API application (on command line)
# !uvicorn main:app --reload


# 5. Test the API application (on browser)
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc UI)
