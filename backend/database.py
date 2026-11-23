from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DATABASE_URL = "sqlite:///./workshopflow.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==========================================
# DATABASE MIGRATION
# ==========================================

def migrate_database():

    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    with engine.begin() as connection:

        # USERS TABLE
        if "users" in existing_tables:

            user_columns = {
                column["name"]
                for column in inspector.get_columns("users")
            }

            if "phone" not in user_columns:
                connection.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN phone VARCHAR(20)"
                    )
                )

                print("Successfully added users.phone")

        # JOB CARDS TABLE
        if "job_cards" in existing_tables:

            job_columns = {
                column["name"]
                for column in inspector.get_columns("job_cards")
            }

            if "created_at" not in job_columns:
                connection.execute(
                    text(
                        "ALTER TABLE job_cards "
                        "ADD COLUMN created_at DATETIME"
                    )
                )

                print("Successfully added job_cards.created_at")

    print("Database migration completed!")


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_db():

    # Create missing tables
    Base.metadata.create_all(bind=engine)

    # Update existing tables
    migrate_database()

    print("WorkshopFlow database initialized successfully!")
