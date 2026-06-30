from app.models.transaction import Transaction
from app.repositories.base_repository import BaseRepository

class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Transaction)

    def get_by_merchant(self, merchant_id):
        return self.model.query.filter_by(merchant_id=merchant_id).order_by(self.model.created_time.desc()).all()

    def get_by_temporary_token(self, token):
        return self.model.query.filter_by(temporary_token=token).first()
