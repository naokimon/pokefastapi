import uvicorn
from api import app
import asyncio
from db import init_db

asyncio.run(init_db())
uvicorn.run(app, host="0.0.0.0", port=8000)