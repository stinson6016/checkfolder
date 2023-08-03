from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_mail import Mail
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
# mail = Mail()
api = Api()