from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, Response
from app.routes.pokemon import router
from scripts.seed_db import init_db
from app.ratelimit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

async def rate_limit_exceeded_handler(
    request: Request,
    exc: Exception,
) -> Response:
    return _rate_limit_exceeded_handler(request, exc)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    rate_limit_exceeded_handler,
)


app.include_router(router)


@app.get("/")
@limiter.limit("2/1second")
async def read_root(request: Request):
    return {"Root": "This is the root of the API."}