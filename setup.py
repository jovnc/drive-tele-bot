# Google API Libraries
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Telegram API Libraries
from telegram.ext import Application

# Misc Libraries
from dotenv import load_dotenv
import logging
import os
import csv

# Set up environment variables
load_dotenv()

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE_PATH')
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Telegram Bot API setup
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation
SELECT_FOLDERS, ENTER_EMAIL = range(2)

# Parse Folders CSV
folders = []
with open('folders.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
        folders.append([row['Folder Name'], row['Folder ID']])

app = Application.builder().token(TELEGRAM_TOKEN).build()