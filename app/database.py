import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@db:5432/pokemon"

for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        break
    except Exception as e:
        print(f"[{i+1}/10] Database not ready, retrying in 2s...")
        time.sleep(2)
else:
    raise RuntimeError("Could not connect to the database after 10 attempts.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
