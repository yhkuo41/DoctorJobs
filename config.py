import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LINE Bot config
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
