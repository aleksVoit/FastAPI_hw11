import redis.asyncio as redis
import uvicorn
from fastapi import Depends, FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from src.routes import contacts, auth, users
from src.conf.config import settings

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Retrieves FastAPI app

    :param app: The number of notes to skip.
    :type app: FastAPI
    """

    print('start app')
    r = await redis.Redis(host=settings.redis_host,
                          port=settings.redis_port,
                          db=0,
                          encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)
    yield
    print('stop app')


app = FastAPI(lifespan=lifespan)

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def read_root():
    """
    Retrieves nothing

    :return: dictionary with message.
    :rtype: Dict
    """
    return {'message': 'Hello World!'}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)

