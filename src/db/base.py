from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
