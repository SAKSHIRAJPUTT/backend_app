import aiosmtplib
import pyjwt
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta

# Define the SMTP settings (example: Gmail SMTP server)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@example.com"
SMTP_PASSWORD = "your_email_password"

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
    secret_key = "your_secret_key"  # This should be a secret key stored securely
    token = pyjwt.encode(payload, secret_key, algorithm="HS256")
    return token

# Example usage:
async def main():
    email = "user@example.com"
    token = generate_verification_token(email)
    await send_verification_email(email, token)

# If you want to run this directly (in an async loop), you can:
# import asyncio
# asyncio.run(main())
