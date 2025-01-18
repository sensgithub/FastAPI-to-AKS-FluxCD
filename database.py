import os
from dotenv import load_dotenv
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

engine = _sql.create_engine(DB_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
