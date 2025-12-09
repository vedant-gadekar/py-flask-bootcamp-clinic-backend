from app.utils.auth_utils import hash_password, verify_password, create_access_token
from app.repositories.repositories import UserRepository


class AuthService:
    @staticmethod
    def register_user(email: str, password: str, role: str):
        existing = UserRepository.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        pwhash = hash_password(password)
        user = UserRepository.create_user(email=email, password=pwhash, role=role)
        return user

    @staticmethod
    def login_user(email: str, password: str):
        user = UserRepository.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        if not verify_password(password, user.password):
            raise ValueError("Invalid credentials")
        token = create_access_token(user.id, user.role)
        return token, user
