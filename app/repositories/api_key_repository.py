from app.models.api_key import ApiKey
from app.repositories.base_repository import BaseRepository

class ApiKeyRepository(BaseRepository):
    def __init__(self):
        super().__init__(ApiKey)

    def get_by_public_key(self, public_key):
        return self.model.query.filter_by(public_key=public_key, is_active=True).first()

    def get_by_user_id(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()
