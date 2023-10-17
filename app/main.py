from fastapi import FastAPI, APIRouter
from app.routers import users

app = FastAPI()

app.include_router(
    router=users.router,
    prefix="/api"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
