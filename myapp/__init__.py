from flask import Flask, render_template
from dotenv import load_dotenv

from .extensions import db, migrate, api
from .apilog import AddChangeLog

def create_app():
    import os

    load_dotenv()
    DB_SERVER = os.getenv('DB_SERVER')
    SECRET_KEY = os.getenv('SECRET_KEY')

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_SERVER
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # import url pages
    from .home import home

    # blueprint register
    app.register_blueprint(home)
    api.add_resource(AddChangeLog, '/api/watch')
       
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template("500.html"), 500
    
    return app