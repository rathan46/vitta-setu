from app.repositories import transaction_repo
from datetime import datetime, timedelta
from sqlalchemy import func

class DashboardService:
    @staticmethod
    def get_dashboard_stats(merchant_id):
        # We'd ideally use SQLAlchemy queries, here's a simplified version.
        # This will be enhanced in a full production setting to run proper SQL aggregations.
        transactions = transaction_repo.get_by_merchant(merchant_id)
        
        today = datetime.utcnow().date()
        today_txs = [t for t in transactions if t.created_time.date() == today]
        
        today_revenue = sum(float(t.amount) for t in today_txs if t.payment_status == 'SUCCESS')
        total_revenue = sum(float(t.amount) for t in transactions if t.payment_status == 'SUCCESS')
        
        success_count = sum(1 for t in transactions if t.payment_status == 'SUCCESS')
        failed_count = sum(1 for t in transactions if t.payment_status == 'FAILED')
        unknown_count = sum(1 for t in transactions if t.payment_status == 'UNKNOWN')
        
        success_rate = (success_count / len(transactions) * 100) if transactions else 0

        return {
            "today_transactions": len(today_txs),
            "today_revenue": today_revenue,
            "total_revenue": total_revenue,
            "success_rate": round(success_rate, 2),
            "successful_payments": success_count,
            "failed_payments": failed_count,
            "unknown_payments": unknown_count,
            "total_transactions": len(transactions)
        }
