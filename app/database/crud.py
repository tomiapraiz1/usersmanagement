from sqlalchemy.orm import Session

from . import models, schemas

from uuid import uuid4, UUID


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    user_exist = get_user_by_username(db, user.username)
    if user_exist:
        return None

    db_user = models.User(
        id=uuid4(),
        username=user.username,
        hashed_password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: UUID, user: schemas.UserCreate):
    user_exist = get_user_by_id(db, user_id)
    if not user_exist:
        return None
    
    user_exist.username = user.username
    user_exist.hashed_password = user.password
    db.commit()
    db.refresh(user_exist)
    return user_exist

def delete_user(db: Session, user_id: UUID):
    user_exist = get_user_by_id(db, user_id)
    if not user_exist:
        return None
    
    db.delete(user_exist)
    db.commit()
    return user_exist