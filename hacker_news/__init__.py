from sched import scheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from .config import Config

app= Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.from_object(Config)
db= SQLAlchemy(app)
migrate= Migrate(app, db)
scheduler= APScheduler()
scheduler.init_app(app)
scheduler.start()

from . import models
from . import custom_functions
from .routes import pages, apis

