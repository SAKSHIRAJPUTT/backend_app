import uvicorn
from backend_app.main import app  # Adjust the import path based on your directory structure

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
