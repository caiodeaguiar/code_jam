from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 🔓 Permitir requisições de qualquer origem (para testes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, especifique domínios seguros
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Login(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/login")
def authenticate(login: Login):
    # Aqui você geraria e retornaria o JWT, por exemplo
    token = f"fake-jwt-for-{login.username}"
    return {"token": token}
