from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def get_session(dbpath='sqlite:///test.db'):
    engine = create_engine(dbpath)
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    return Session()
