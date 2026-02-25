from models import init_db, migrate_from_json

def main():
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    
    print("Running data migration if needed...")
    migrate_from_json()
    print("Data migration completed!")

if __name__ == "__main__":
    main()
