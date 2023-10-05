import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.getenv('MONGO_URL')
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    MIXPANEL_TOKEN = os.getenv("MIXPANEL_TOKEN")
