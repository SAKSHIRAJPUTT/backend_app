import requests
from sqlalchemy.orm import Session
from . import models, database
from passlib.context import CryptContext
import os

# Initialize the password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def import_mock_data(db: Session):
    # Get the API Key from environment variables (or use a configuration file)
    api_key = os.getenv("MOCKAROO_API_KEY")
    if not api_key:
        raise ValueError("API key for Mockaroo not set. Please set MOCKAROO_API_KEY in environment variables.")
    
    # Make the request to the Mockaroo API
    url = f"https://api.mockaroo.com/api/{api_key}?count=100&key={api_key}"
    response = requests.get(url)
    
    # Check if the response is successful (status code 200)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch mock data. Status code: {response.status_code}")
    
    # Parse the response JSON data
    mock_data = response.json()

    # Iterate over each item in the mock data and create a new user
    for item in mock_data:
        # Hash the password before storing it
        hashed_password = pwd_context.hash(item['password'])
        user = models.User(username=item['username'], password=hashed_password)
        
        db.add(user)

    # Commit the transaction to the database
    try:
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback if there is an error during commit
        raise Exception(f"Error while committing data to the database: {str(e)}")

