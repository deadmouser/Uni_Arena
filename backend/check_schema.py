from sqlalchemy import create_engine, inspect
# Assuming sqlite for now if import fails, or use get_db logic?
# Let's inspect the database file directly if possible, or use the Base from models?
# Actually, I can just hardcode the URL which is standard.
SQLALCHEMY_DATABASE_URL = "sqlite:///./uni_arena.db"

def check_schema():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    inspector = inspect(engine)
    
    if "sports" in inspector.get_table_names():
        columns = [c["name"] for c in inspector.get_columns("sports")]
        print(f"Sports table columns: {columns}")
        
        missing = []
        for required in ["rules", "match_config", "mandatory_rules"]:
            if required not in columns:
                missing.append(required)
        
        if missing:
            print(f"MISSING COLUMNS: {missing}")
        else:
            print("Schema looks correct.")
    else:
        print("Sports table does not exist.")

if __name__ == "__main__":
    check_schema()
