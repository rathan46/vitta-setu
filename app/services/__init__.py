from app.services.auth_service import AuthService
from app.services.api_key_service import ApiKeyService
from app.services.payment_service import PaymentService
from app.services.callback_service import CallbackService
from app.services.dashboard_service import DashboardService

auth_service = AuthService()
api_key_service = ApiKeyService()
payment_service = PaymentService()
callback_service = CallbackService()
dashboard_service = DashboardService()
