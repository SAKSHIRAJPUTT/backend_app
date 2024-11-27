from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models

def analyze_user_data(db: Session):
    # Total number of users
    total_users = db.query(models.User).count()
    
    # Users per month (for SQLite)
    # Replace with appropriate logic for your DB if not using SQLite
    users_per_month = (
        db.query(
            func.strftime('%Y-%m', models.User.created_at).label("month"), 
            func.count(models.User.id).label("count")
        )
        .group_by(func.strftime('%Y-%m', models.User.created_at))
        .all()
    )
    
    # If you're using PostgreSQL, you might want to replace the `strftime` with:
    # users_per_month = (
    #     db.query(
    #         func.date_trunc('month', models.User.created_at).label("month"),
    #         func.count(models.User.id).label("count")
    #     )
    #     .group_by(func.date_trunc('month', models.User.created_at))
    #     .all()
    # )
    
    return {
        "total_users": total_users,
        "users_per_month": users_per_month
    }
