from app.models.models import User
from app.config.db import db

class UserRepository:
    @staticmethod
    def create_user(email: str, password: str, role: str) -> User:
        user = User(email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id: int):
        return db.session.get(User, user_id)



