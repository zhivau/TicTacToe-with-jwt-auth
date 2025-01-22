from flask_sqlalchemy import SQLAlchemy
from config import settings
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL_psycopg
    app.config["SаQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
