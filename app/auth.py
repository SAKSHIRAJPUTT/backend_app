import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas, models, database
from fastapi.security import OAuth2PasswordBearer

# OAuth2 password bearer for token management
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT Secret key and algorithm
SECRET_KEY = "your_secret_key"  # Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Exception for invalid credentials (JWT token)
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Password verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Password hashing
def get_password_hash(password):
    return pwd_context.hash(password)

# JWT token creation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default expiration time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Extract the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Fetch the user from the database using the username from the token
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Role-based access control: restrict access based on role
def role_required(role_name: str):
    def role_checker(current_user: schemas.User = Depends(get_current_user)):
        if current_user.role.name != role_name:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user
    return role_checker
