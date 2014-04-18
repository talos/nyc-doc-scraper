import requests
import sys
from zipfile import ZipFile, ZIP_DEFLATED


def scrape(start_num, end_num):
    with ZipFile('archive.zip', 'w', compression=ZIP_DEFLATED) as archive:
        for n in xrange(start_num, end_num + 1):
            resp = requests.get(
                u'http://appext20.dos.ny.gov/corp_public/CORPSEARCH.ENTITY_INFORMATION?p_nameid=1&p_corpid={}&p_entity_name=a%20real&p_name_type=A&p_search_type=BEGINS'.format(n))
            archive.writestr('{}.html'.format(n), resp.content)


if __name__ == '__main__':
    scrape(int(sys.argv[1]), int(sys.argv[2]))
