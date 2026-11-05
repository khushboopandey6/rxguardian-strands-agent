# config.py - Settings for RxGuardian project
# Written by Khushboo for the AWS Strands Hackathon

import os
from dotenv import load_dotenv

# Load secret keys or environment variables from .env file if it exists
load_dotenv()

# AWS settings for Bedrock
# We use us-east-1 by default, but you can change it in .env
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", "")

# The Bedrock AI model we want to use (Claude 3.5 Sonnet is great for medical safety)
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")

# Check if the user gave us real AWS keys
# If not, no problem! We run our smart local simulation so anyone can test it for free!
HAS_BEDROCK_CREDENTIALS = bool(
    (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) or
    os.getenv("AWS_PROFILE") or
    os.getenv("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI")
)

# Web server settings
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = True
