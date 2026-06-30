from app.repositories import user_repo
from datetime import datetime

class AuthService:
    def register_merchant(self, email, password, merchant_name, owner_name, business_name):
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            return False, "Email already registered"

        user = user_repo.create(
            email=email,
            merchant_name=merchant_name,
            owner_name=owner_name,
            business_name=business_name
        )
        user.set_password(password)
        user_repo.update(user)
        return True, user

    def authenticate(self, email, password):
        user = user_repo.get_by_email(email)
        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            user_repo.update(user)
            return True, user
        return False, "Invalid credentials"
