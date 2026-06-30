from app.models.payment_session import PaymentSession
from app.repositories.base_repository import BaseRepository

class PaymentSessionRepository(BaseRepository):
    def __init__(self):
        super().__init__(PaymentSession)

    def get_by_token(self, token):
        return self.model.query.filter_by(temporary_token=token).first()
