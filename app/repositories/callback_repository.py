from app.models.callback_log import CallbackLog
from app.repositories.base_repository import BaseRepository

class CallbackRepository(BaseRepository):
    def __init__(self):
        super().__init__(CallbackLog)

    def get_by_transaction_id(self, transaction_id):
        return self.model.query.filter_by(transaction_id=transaction_id).all()
