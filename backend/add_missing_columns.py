import sqlite3

DB_FILE = "uni_arena.db"

def add_columns():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    columns = [
        ("rules", "TEXT"),
        ("match_config", "TEXT"),
        ("mandatory_rules", "TEXT")
    ]
    
    for col_name, col_type in columns:
        try:
            print(f"Adding column {col_name}...")
            cursor.execute(f"ALTER TABLE sports ADD COLUMN {col_name} {col_type}")
            print(f"Successfully added {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists")
            else:
                print(f"Error adding {col_name}: {e}")
                
    conn.commit()
    conn.close()
    print("Schema update complete.")

if __name__ == "__main__":
    add_columns()
