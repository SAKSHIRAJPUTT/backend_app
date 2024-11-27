from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Add password field
    created_at = Column(DateTime, default=func.now())  # Timestamp for user creation

    # Example of a relationship to a 'Role' table, if applicable
    # roles = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, created_at={self.created_at})>"
