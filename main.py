from typing import Optional
import uvicorn
from fastapi import FastAPI
from models.user import *
from db.config import *
from routers import user_router
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(user_router.router)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def Home():
    return "Bem vindo a API-REST da GALATIKA-SHOP"

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Galatika-Shop Documentation",
        version="0.1",
        description="API do E-commerce da Galatika",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

    
app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)