import requests
from sqlalchemy.orm import Session
from . import models, database

def import_mock_data(db: Session):
    response = requests.get("https://api.mockaroo.com/api/YOUR_API_KEY?count=100&key=YOUR_API_KEY")
    mock_data = response.json()
    
    for item in mock_data:
        user = models.User(username=item['username'], password=item['password'])
        db.add(user)
    db.commit()