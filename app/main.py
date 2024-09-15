from fastapi import FastAPI

from app.database import init_db
from app.users.router import router

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()
