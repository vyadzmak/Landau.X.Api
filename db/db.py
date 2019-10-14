
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from settings import DB_URI

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI, pool_size=20, max_overflow =20))
session = scoped_session(Session)

