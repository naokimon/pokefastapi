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

uvicorn.run(app, host="0.0.0.0", port=8000)