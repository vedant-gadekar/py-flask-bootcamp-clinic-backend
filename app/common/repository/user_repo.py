from app.common.models.user import User
from app.config.database import db

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
    
    @staticmethod
    def update_role(user_id: int, new_role: str):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        user.role = new_role
        db.session.commit()
        return user




