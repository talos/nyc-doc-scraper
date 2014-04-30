from models import Entity, Name, Address, EntityTitle, StockInformation, \
        NameHistory, Title

import sys
import logging
import re

from datetime import datetime
from database import get_session
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from cssselect import GenericTranslator
from lxml import etree
from zipfile import ZipFile

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

tableselector = GenericTranslator().css_to_xpath('table')
trselector = GenericTranslator().css_to_xpath('tr')
thselector = GenericTranslator().css_to_xpath('th')
tdselector = GenericTranslator().css_to_xpath('td')


def css_select(self, html, selector, as_strings=True):
    """
    Select string via CSS selector from text.  If `as_strings` is True (the
    default, then it returns a list of strings, otherwise it returns a list
    of lxml elements.
    """
    tree = etree.HTML(html.decode('utf-8'))
    elements = tree.xpath(GenericTranslator().css_to_xpath(selector))
    if as_strings:
        return map(etree.tostring, elements)
    else:
        return elements


def totext(element):
    return collapse_ws(etree.tostring(element, method='text', encoding='utf-8').decode('utf-8'))


def collapse_ws(text):
    """
    Collapse internal whitespace & trim leading & trailing whitespace
    """
    return re.sub(r'[ \t\f\v]+', u' ', text).strip()


def parse(session, content):
    start = datetime.now()
    try:
        tree = etree.HTML(content.decode('WINDOWS-1252'))
    except UnicodeDecodeError:
        tree = etree.HTML(content.decode('latin1'))

    tables = tree.xpath(tableselector)
    status_table, address_table, stock_table, name_history_table = tables

    name, dos_id_num, dos_filing_date, county, jurisdiction, entity_type, \
            current_entity_status = [totext(td) for td in status_table.xpath(tdselector)]

    if not dos_id_num:
        return

    try:
        dos_filing_date = datetime.strptime(dos_filing_date, '%b %d, %Y') if dos_filing_date else None
    except ValueError:
        dos_filing_date = datetime.strptime(dos_filing_date, '%B %d, %Y') if dos_filing_date else None


    try:
        entity = Entity(dos_id=dos_id_num, current_entity_name=name,
                        initial_dos_filing_date=dos_filing_date,
                        county=county, jurisdiction = jurisdiction,
                        entity_type=entity_type, current_entity_status=current_entity_status)
        session.add(entity)

        address_table_headers = address_table.xpath(thselector)
        address_table_columns = address_table.xpath(tdselector)

        for i, h in enumerate(address_table_headers):
            addrs = totext(address_table_columns[i]).split(u'\n')

            title_str = totext(address_table_headers[i])
            title = session.query(Title).filter(Title.title == title_str).first() \
                    or Title(title=title_str)

            address_str = u'\n'.join(addrs[1:])
            address = session.query(Address).filter(Address.address == address_str).first() \
                    or Address(address=address_str)

            name_str = addrs[0]
            name = session.query(Name).filter(Name.name == name_str).first() \
                    or Name(name=name_str)

            entity_title = EntityTitle(entity=entity, title=title,
                                       address=address, name=name)

            session.add(entity_title)

        stock_rows = stock_table.xpath(trselector)

        for i, row in enumerate(stock_rows):
            if i > 0:
                cols = row.xpath(tdselector)
                session.add(StockInformation(
                    entity=entity,
                    num_of_shares=totext(cols[0]) or None,
                    type_of_stock=totext(cols[1]),
                    dollar_value_per_share=totext(cols[2])
                ))

        name_history_rows = name_history_table.xpath(trselector)

        for i, row in enumerate(name_history_rows):
            if i > 0:
                cols = row.xpath(tdselector)
                datecol = totext(cols[0])
                session.add(NameHistory(
                    entity=entity,
                    filing_date=datetime.strptime(datecol, '%b %d, %Y') if datecol else None,
                    name_type=totext(cols[1]),
                    entity_name=totext(cols[2])
                ))

        #print('processed {} in {}'.format(dos_id_num, datetime.now() - start))
        session.commit()
    except InvalidRequestError as e:
        logger.debug(e)
        logger.info('Skipped {} (InvalidRequestError)'.format(dos_id_num))
        session.rollback()
    except IntegrityError as e:
        logger.debug(e)
        logger.info('Skipped {} (IntegrityError)'.format(dos_id_num))
        session.rollback()
    except DataError as e:
        logger.debug(e)
        logger.info('Skipped {} (DataError)'.format(dos_id_num))
        session.rollback()


if __name__ == '__main__':
    session = get_session(sys.argv[1])
    min_id = int(sys.argv[3]) or None
    with ZipFile(sys.argv[2], 'r') as archive:
        for name in archive.namelist():
            if name.endswith('.html'):
                if min_id:
                    dos_id = int(name.replace('.html', ''))
                    if dos_id < min_id:
                        continue
                try:
                    parse(session, archive.open(name).read())
                except Exception as e:
                    logger.error("Could not parse {}: {}".format(dos_id, e))
                    session.rollback()
        session.commit()
