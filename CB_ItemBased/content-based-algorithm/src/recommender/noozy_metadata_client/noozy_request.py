'''
Created on 18 mars 2021
Request class with methods to request Noozy REDIS repository

@author:     Azim Roussanaly
@copyright:  2021 LORIA/Université de Lorraine. All rights reserved.
@license:    GNU General Public License, Version 3
@contact:    azim.roussanaly@loria.fr
@deffield    updated: Mar, 18, 2021'''
import configparser
import logging
from rejson.client import Client
import traceback
import datetime
import pytz
import configparser
import logging
import os
import sys


class NoozyRequest:
    '''
    Request class with following methods:
    - getIdList
    '''
    def __init__(self) -> None:

        self.filename = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "config/noozy.ini")

        self.config = configparser.ConfigParser()
        logging.debug("reading config file : " + self.filename)

        self.config.read(self.filename)

        self.host = self.config["REDIS"]["Host"]
        self.port = self.config["REDIS"]["Port"]
        self.password = self.config["REDIS"]["Password"]

        logging.info(self.host)

        try:
            if not self.password:
                self.client = Client(host=self.host, port=self.port, decode_responses=True)
            else:
                self.client = Client(host=self.host, port=self.port, password=self.password, decode_responses=True)
                self.client.ping()
                logging.info("redis4harvest connected")
        except Exception as e:
            logging.error(f"ERREUR : Impossible de créer un client REDIS: {str(e)}")
            raise

    def get_ids(self, date=None):
        '''
        get the list of (id,datetime)
        :param date : the oldest available item (based on dc:available date field)
        '''
        res = []
        n = 0
        for k in self.client.keys():
            try:
                v = self.client.jsonget(k)['dc:available']
                d = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S%z")
                if d >= date:
                    res.append((k, d))
                    n += 1
            except Exception as e:
                logging.warning(f'error in: {k} (ignored)')
                logging.warning(f'message: {str(e)}')
        logging.debug(f'selected {n} items')
        return res

    def get_items(self, date=None):
        '''
        get the list of (id,datetime)
        :param date : the oldest available item (based on dc:available date field)
        :param parameters: if None, will only return dc:identifier
        :returns metadata
        '''
        vp = {}
        res = []
        n = 0
        for k in self.client.keys():
            try:
                v = self.client.jsonget(k)
                d = datetime.datetime.strptime(v['dc:available'], "%Y-%m-%dT%H:%M:%S%z")
                if d >= date:
                    res.append(v)
                    n += 1
            except Exception as e:
                logging.warning(f'error in: {k} (ignored)')
                logging.warning(f'message: {str(e)}')
        logging.debug(f'selected {n} items')
        # print(res)
        return res


# ===============================================================================
# test
# ===============================================================================
def test():
    try:
        r = NoozyRequest()
        utc = pytz.UTC
        date = utc.localize(datetime.datetime(2021, 1, 1))
        l = r.getIds(date)
        print(l)
    except Exception as e:
        logging.error(e)
        traceback.print_exc()


def test2():
    try:
        r = NoozyRequest()
        utc = pytz.UTC
        date = utc.localize(datetime.datetime(2021, 1, 1))
        l = r.getItems(date)
        print(l)
    except Exception as e:
        logging.error(e)
        traceback.print_exc()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
    # test()
    test2()
