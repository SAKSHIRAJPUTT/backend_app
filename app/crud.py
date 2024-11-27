from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    # Hash the password before saving to the database
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    
    # Check if the user already exists (optional, but good practice)
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise ValueError("Username already exists.")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    # Find user by ID, returns None if not found
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    # Retrieve list of users with pagination
    return db.query(models.User).offset(skip).limit(limit).all()
