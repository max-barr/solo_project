from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = str(os.getenv("SECRET_KEY"))

API_KEY = str(os.getenv("API_KEY"))
