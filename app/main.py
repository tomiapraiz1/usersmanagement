from fastapi import FastAPI, APIRouter
from app.database import models
from app.database.database import engine
from app.routers import users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(
    router=users.router,
    prefix="/api"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
