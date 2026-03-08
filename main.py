from fastapi import FastAPI, Request
from routers.movie_router import router as movie_router
from routers.user_router import router as auth_router

import logging


app = FastAPI(title="Secure Movie Library")
logging.basicConfig(level=logging.INFO)


app.include_router(auth_router)
app.include_router(movie_router)
