from flask import Flask
from app.config import DefaultConfig

app = Flask(__name__)
app.config.from_object(DefaultConfig)

from app import routes