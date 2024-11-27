from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend_app import models, schemas, crud, database, auth, data_import
from backend_app.models import User
from fastapi import OAuth2PasswordRequestForm
from . import crud, models, database

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    pass

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud .create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/data-analysis/")
def analyze_data(db: Session = Depends(database.get_db)):
    # Mock data analysis logic
    # Here you would typically query your database and perform analysis
    analyzed_data = {"total_users": db.query(models.User).count()}
    return analyzed_data

#Create the database tables if they don't exist
database.Base.metadata.create_all(bind=database.engine)

@app.post("/import-data/")
def import_data(num_users: int = 100, db: Session = Depends(database.get_db)):
    data_import.import_mock_data(db, num_users)
    return {"message": f"{num_users} users imported successfully"}

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/import-data/")
def import_data(db: Session = Depends(database.get_db)):
    import_mock_data(db)
    return {"message": "Data imported successfully"}

@app.get("/data-analysis/")
def analyze_data(db: Session = Depends(database.get_db)):
    analyzed_data = analyze_user_data(db)
    return analyzed_data

 
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/data-analysis/")
async def data_analysis():
    data = {
        "users_per_month": {
            "January": 100,
            "February": 150,
            "March": 120,
            "April": 130,
        }
    }
    return JSONResponse(content=data)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, role_id: int, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user, role_id=role_id)

@app.get("/admin/")
def read_admin_data(current_user: schemas.User = Depends(role_required("admin"))):
    return {"message": "Welcome to the admin area!"}

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter

@app.get("/limited/")
@limiter.limit("5/minute")
def limited_endpoint():
    return {"message": "This endpoint is rate limited."}

from fastapi import FastAPI, HTTPException
import pyjwt
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI()

# Secret key to decode the JWT token (ensure this matches the key used during encoding)
SECRET_KEY = "your_secret_key"  # Store this securely (use environment variables)

@app.get("/verify")
async def verify_email(token: str):
    try:
        # Decode the JWT token
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Check if the token has expired
        if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(status_code=400, detail="Token expired")

        # If the token is valid, retrieve the email
        email = payload["email"]

        # Perform email verification logic (e.g., updating the user record in the database)
        # Example: Mark the user's email as verified
        # For example, assuming you have a User model and DB session
        # db = get_db()  # your database session
        # user = db.query(User).filter(User.email == email).first()
        # if user:
        #     user.is_verified = True
        #     db.commit()

        return {"message": f"Email {email} verified successfully"}

    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyjwt
from datetime import datetime, timedelta
import aiosmtplib  # Used for sending emails
from fastapi.responses import JSONResponse

app = FastAPI()

SECRET_KEY = "your_secret_key"  # Use a secure key for your production app
EMAIL_SENDER = "your_email@example.com"  # Sender email address

class User(BaseModel):
    email: str
    username: str
    password: str

async def send_verification_email(email: str, token: str):
    subject = "Email Verification"
    body = f"Please verify your email by clicking on the following link: http://yourdomain.com/verify?token={token}"
    message = f"Subject: {subject}\n\n{body}"
    
    # Send the email (replace with your SMTP configuration)
    await aiosmtplib.send(message, to=email, from_addr=EMAIL_SENDER)

@app.post("/register/")
async def register_user(user: User):
    # You would typically save the user data in the database here
    # For now, assume the registration is successful

    # Generate a verification token
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    token = pyjwt.encode({"email": user.email, "exp": expiration}, SECRET_KEY, algorithm="HS256")

    # Send the verification email
    await send_verification_email(user.email, token)

    return {"message": "User registered successfully! Please check your email to verify your account."}
