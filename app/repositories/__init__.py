from app.repositories.user_repository import UserRepository
from app.repositories.api_key_repository import ApiKeyRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.payment_session_repository import PaymentSessionRepository
from app.repositories.callback_repository import CallbackRepository

user_repo = UserRepository()
api_key_repo = ApiKeyRepository()
transaction_repo = TransactionRepository()
payment_session_repo = PaymentSessionRepository()
callback_repo = CallbackRepository()
