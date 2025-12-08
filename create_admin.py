"""
create_admin.py - Secure Admin Creation Script
"""
from backend.shared.database import SessionLocal
from backend.shared.models import User, UserRole
from passlib.context import CryptContext
from datetime import datetime
import getpass  # ← For secure password input

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()
    
    try:
        # Get credentials securely
        admin_email = input("Enter admin email: ").strip()
        admin_password = getpass.getpass("Enter admin password: ")  # Hidden input
        admin_name = input("Enter admin full name: ").strip()
        
        # Validate
        if not admin_email or not admin_password:
            print("❌ Email and password are required!")
            return
        
        # Check if already exists
        if db.query(User).filter(User.email == admin_email).first():
            print(f"❌ User with email '{admin_email}' already exists!")
            return
        
        # Create admin
        admin_user = User(
            email=admin_email,
            password_hash=pwd_context.hash(admin_password),
            full_name=admin_name,
            role=UserRole.ADMIN,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        
        print("\n✅ Admin user created successfully!")
        print(f"📧 Email: {admin_email}")
        print(f"👤 Name: {admin_name}")
        print(f"🆔 Role: ADMIN")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()