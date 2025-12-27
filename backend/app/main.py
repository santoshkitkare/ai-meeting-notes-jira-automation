from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.db import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Meeting → Jira")

app.include_router(router)

@app.get("/")
def health():
    return {"status": "running"}
