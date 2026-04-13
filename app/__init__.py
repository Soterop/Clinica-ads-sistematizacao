from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = 'brasília-2026-sistematizacao'


uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


app.config['SQLALCHEMY_DATABASE_URI'] = uri or 'postgresql://usuario:123456@localhost:5432/clinica'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
