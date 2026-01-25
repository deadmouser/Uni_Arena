"""Quick test to verify database connection"""
import sys
from database import SessionLocal, engine, Base
from models.auth import User

# Force output
print("Testing database connection...", flush=True)

try:
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully", flush=True)
    
    # Test connection
    db = SessionLocal()
    user_count = db.query(User).count()
    print(f"✅ Database connection successful. Current users: {user_count}", flush=True)
    db.close()
    
    print("\n✅ Database is ready. You can now run: python seed_data.py", flush=True)
except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
