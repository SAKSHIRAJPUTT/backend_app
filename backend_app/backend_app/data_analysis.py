from sqlalchemy import func

def analyze_user_data(db: Session):
    total_users = db.query(models.User).count()
    # Example of more complex analysis
    users_per_month = db.query(func.strftime('%Y-%m', models.User.created_at)).group_by(func.strftime('%Y-%m', models.User.created_at)).count()
    return {
        "total_users": total_users,
        "users_per_month": users_per_month
    }