from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import crud, models, schemas
from app.database.database import get_db, engine

from uuid import UUID

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=list[schemas.User])
async def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return user


@router.put("/{user_id}")
async def update_user(user_id: UUID, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_updated = crud.update_user(db, user_id, user)
    if user_updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User updated successfully"}


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user_deleted = crud.delete_user(db, user_id)
    if user_deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}
