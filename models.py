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

    addresses = relationship('Address', secondary='entity_addresses',
                             back_populates='entities')
    stockinformation = relationship('StockInformation', backref='entity')
    namehistory = relationship('NameHistory', backref='entity')

    current_through = Column(DateTime())


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer(), primary_key=True)

    addr1 = Column(String(STRING_SZ))
    addr2 = Column(String(STRING_SZ))
    addr3 = Column(String(STRING_SZ))

    entities = relationship('Entity', secondary='entity_addresses',
                            back_populates='addresses')


class EntityAddress(Base):
    __tablename__ = 'entity_addresses'

    id = Column(Integer(), primary_key=True)

    entity_id = Column(Integer(), ForeignKey('entities.dos_id'))
    address_id = Column(Integer(), ForeignKey('addresses.id'))

    title = Column(String())


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
