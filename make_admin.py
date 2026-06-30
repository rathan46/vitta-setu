import sys
from run import app
from app.extensions import db
from app.models.user import User

def make_admin(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return

        if user.is_admin:
            print(f"User '{email}' is already an admin.")
            return
            
        user.is_admin = True
        user.account_status = 'active'
        db.session.commit()
        
        print(f"Success! '{email}' has been promoted to Administrator.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <user_email>")
        sys.exit(1)
        
    make_admin(sys.argv[1])
