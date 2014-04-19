from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Entity, Address, EntityAddress, StockInformation, \
        NameHistory, Base

engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
session = Session()

