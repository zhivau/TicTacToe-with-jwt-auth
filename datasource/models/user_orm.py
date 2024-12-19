from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UUID
from datasource.database import db


class UserORM(db.Model):
    __tablename__ = "users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.login}"
