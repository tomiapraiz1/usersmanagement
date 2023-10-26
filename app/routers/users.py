from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import user_service, schemas
from app.database.database import get_db

from uuid import UUID

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=list[schemas.User])
async def get_all_users(db: db_dependency):
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: UUID, db: db_dependency):
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: db_dependency):
    user = user_service.create_user(db, user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return user


@router.put("/{user_id}")
async def update_user(user_id: UUID, user: schemas.UserCreate, db: db_dependency):
    user_updated = user_service.update_user(db, user_id, user)
    if user_updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User updated successfully"}


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: db_dependency):
    user_deleted = user_service.delete_user(db, user_id)
    if user_deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}
