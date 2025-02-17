from flask import Flask
from flask_pymongo import PyMongo
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/StoryWeavePy"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=30)
mongodb = PyMongo(app).db

