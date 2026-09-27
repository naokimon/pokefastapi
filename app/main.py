import uvicorn
import asyncio
from fastapi import FastAPI
from scripts.seed_db import init_db
from app.routes.pokemon import router as pokemon_router

asyncio.run(init_db())

app = FastAPI()

@app.get("/")
def read_root():
    return {"Root": "This is the root of the API."}

app.include_router(pokemon_router)

uvicorn.run(app, host="127.0.0.1", port=8000, proxy_headers=True, forwarded_allow_ips="127.0.0.1")