from typing import Optional
import uvicorn
from fastapi import FastAPI
from models.usuario import *
from db.config import *
from routers import router

app = FastAPI()
app.include_router(router.router)

@app.get("/")
async def Home():
    return "Bem vindo a API-REST da GALATIKA-SHOP"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)