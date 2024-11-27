from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        # Ensures that the model can be serialized from an ORM object (e.g., SQLAlchemy)
        orm_mode = True

class User(BaseModel):
    id: int
    username: str

    class Config:
        # Ensures that the model can be serialized from an ORM object (e.g., SQLAlchemy)
        orm_mode = True
