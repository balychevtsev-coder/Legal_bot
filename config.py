import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_CREDS_PATH = "grand-analyzer-477015-m9-3ea9c9329efb.json"