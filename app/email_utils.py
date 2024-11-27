import aiosmtplib
import jwt
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta
import os

# Define the SMTP settings (these should ideally be stored in environment variables for security)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER", "your_email@example.com")  # Retrieve from environment variable
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_email_password")  # Retrieve from environment variable

# Function to validate email
def validate_user_email(email: str):
    try:
        validate_email(email)  # This will raise EmailNotValidError if the email is invalid
    except EmailNotValidError as e:
        raise ValueError(f"Invalid email address: {e}")

# Async function to send verification email
async def send_verification_email(email: str, token: str):
    subject = "Email Verification"
    body = f"Please verify your email by clicking on the following link: http://yourdomain.com/verify?token={token}"
    message = f"Subject: {subject}\n\n{body}"

    try:
        # Sending the email asynchronously
        await aiosmtplib.send(
            message,
            to=email,
            from_addr=SMTP_USER,
            host=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True
        )
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to generate JWT token
def generate_verification_token(email: str):
    # Create a payload with the email and expiration time
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    payload = {
        "email": email,
        "exp": expiration
    }

    # Generate JWT token
    secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # Secret key should also be retrieved from environment
    token = pyjwt.encode(payload, secret_key, algorithm="HS256")
    return token

# Example usage:
async def main():
    email = "user@example.com"

    # Validate the email before proceeding
    try:
        validate_user_email(email)
    except ValueError as e:
        print(e)
        return  # If the email is invalid, exit the function

    # Generate the verification token
    token = generate_verification_token(email)

    # Send the verification email
    await send_verification_email(email, token)

# If running this script standalone:
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
