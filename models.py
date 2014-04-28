from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

STRING_SZ = 255

class Entity(Base):
    __tablename__ = 'entities'

    dos_id = Column(Integer(), primary_key=True)

    current_entity_name = Column(String(STRING_SZ))
    initial_dos_filing_date = Column(DateTime())
    county = Column(String(STRING_SZ))
    jurisdiction = Column(String(STRING_SZ))
    entity_type = Column(String(STRING_SZ))
    current_entity_status = Column(String(STRING_SZ))

    entity_titles = relationship('EntityTitle', backref='entity')
    stockinformation = relationship('StockInformation', backref='entity')
    namehistory = relationship('NameHistory', backref='entity')

    current_through = Column(DateTime())


class EntityTitle(Base):
    __tablename__ = 'entity_titles'

    entity_id = Column(Integer(), ForeignKey('entities.dos_id'), primary_key=True)
    title_id = Column(Integer(), ForeignKey('titles.id'), primary_key=True)
    name_id = Column(Integer(), ForeignKey('names.id'), primary_key=True)
    address_id = Column(Integer(), ForeignKey('addresses.id'), primary_key=True)


class Title(Base):
    __tablename__ = 'titles'

    id = Column(Integer(), primary_key=True)
    title = Column(String(), unique=True)

    entity_titles = relationship('EntityTitle', backref='title')


class Name(Base):
    __tablename__ = 'names'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), unique=True)

    entity_titles = relationship('EntityTitle', backref='name')


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer(), primary_key=True)
    address = Column(String(), unique=True)

    entity_titles = relationship('EntityTitle', backref='address')


class StockInformation(Base):
    __tablename__ = 'stockinformation'

    id = Column(Integer(), primary_key=True)
    entity_id = Column(Integer(), ForeignKey('entities.dos_id'))

    num_of_shares = Column(Integer())
    type_of_stock = Column(String(STRING_SZ))
    dollar_value_per_share = Column(String(STRING_SZ)) # TODO is this string or int? Float?


class NameHistory(Base):
    __tablename__ = 'namehistory'

    id = Column(Integer(), primary_key=True)
    entity_id = Column(Integer(), ForeignKey('entities.dos_id'))

    filing_date = Column(DateTime())
    name_type = Column(String(STRING_SZ))
    entity_name = Column(String(STRING_SZ))
