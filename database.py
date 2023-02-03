from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = ('sqlite:///databese.sqlite')

engine = create_engine(
    url=DATABASE_URL,
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
