from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from . import models, schemas, crud, database, auth, data_import
from fastapi.security import OAuth2PasswordRequestForm
import jwt
import aiosmtplib
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize FastAPI app
app = FastAPI()

# Secret key and email settings
SECRET_KEY = "your_secret_key"  # Store securely
EMAIL_SENDER = "your_email@example.com"  # Sender email address

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize Limiter for rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


# JWT and Authentication Routes
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/verify")
async def verify_email(token: str):
    try:
        # Decode JWT token
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Check if token is expired
        if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=400, detail="Token expired")

        email = payload["email"]
        # Here, you would mark the email as verified in your database
        # Example: user = db.query(User).filter(User.email == email).first()

        return {"message": f"Email {email} verified successfully"}

    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")


async def send_verification_email(email: str, token: str):
    subject = "Email Verification"
    body = f"Please verify your email by clicking on the following link: http://yourdomain.com/verify?token={token}"
    message = f"Subject: {subject}\n\n{body}"

    # Send email (you'll need to configure your SMTP server)
    await aiosmtplib.send(message, to=email, from_addr=EMAIL_SENDER)


# User Registration and Verification Routes
class User(BaseModel):
    email: str
    username: str
    password: str


@app.post("/register/")
async def register_user(user: User):
    # Simulate user registration in the database
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    token = pyjwt.encode({"email": user.email, "exp": expiration}, SECRET_KEY, algorithm="HS256")

    # Send verification email
    await send_verification_email(user.email, token)

    return {"message": "User registered successfully! Please check your email to verify your account."}


# CRUD Operations for Users
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


# Mock Data Import Route
@app.post("/import-data/")
def import_data(num_users: int = 100, db: Session = Depends(database.get_db)):
    data_import.import_mock_data(db, num_users)
    return {"message": f"{num_users} users imported successfully"}


# Data Analysis Route
@app.get("/data-analysis/")
def analyze_data(db: Session = Depends(database.get_db)):
    analyzed_data = {"total_users": db.query(models.User).count()}
    return analyzed_data


# Admin Role Required Route
@app.get("/admin/")
def read_admin_data(current_user: schemas.User = Depends(auth.role_required("admin"))):
    return {"message": "Welcome to the admin area!"}


# Rate Limiting Example
@app.get("/limited/")
@limiter.limit("5/minute")
async def limited_endpoint(request: Request):
    return {"message": "This endpoint is rate limited."}

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Data Visulaization"}

