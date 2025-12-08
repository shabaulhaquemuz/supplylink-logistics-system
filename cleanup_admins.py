"""
cleanup_admins.py - Remove all admin users with this email
"""
from backend.shared.database import SessionLocal
from backend.shared.models import User

db = SessionLocal()

try:
    # Delete all users with this email
    deleted = db.query(User).filter(
        User.email == 'shabaulhaque2025@gmail.com'
    ).delete()
    
    db.commit()
    print(f"✅ Deleted {deleted} user(s) with email 'shabaulhaque2025@gmail.com'")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()