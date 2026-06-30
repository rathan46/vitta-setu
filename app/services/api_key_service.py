from app.repositories import api_key_repo
from app.utils.security import generate_api_key

class ApiKeyService:
    def generate_keys_for_user(self, user_id):
        public_key, private_secret = generate_api_key()
        api_key = api_key_repo.create(
            user_id=user_id,
            public_key=public_key,
            private_secret=private_secret
        )
        return api_key

    def validate_public_key(self, public_key):
        return api_key_repo.get_by_public_key(public_key)

    def revoke_key(self, key_id):
        api_key = api_key_repo.get_by_id(key_id)
        if api_key:
            api_key.is_active = False
            api_key_repo.update(api_key)
            return True
        return False
