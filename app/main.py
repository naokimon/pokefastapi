from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.pokemon import router
from scripts.seed_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Root": "This is the root of the API."}

app.include_router(router)