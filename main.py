from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes import contacts ,auth

from src.database.db import get_db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contacts.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "TODO API"}