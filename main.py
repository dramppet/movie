from fastapi import FastAPI, Request
from routers.movie_router import router as movie_router
from routers.user_router import router as auth_router
from routers.web_router import router as web_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import logging


app = FastAPI(title="Secure Movie Library")
logging.basicConfig(level=logging.INFO)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(movie_router)
app.include_router(web_router)