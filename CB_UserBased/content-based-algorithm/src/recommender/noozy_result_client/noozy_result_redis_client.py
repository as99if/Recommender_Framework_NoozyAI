import configparser
import json
import logging
import os
import sys

from rejson import Client
from rejson import Path


class NoozyResultStoreClient:

    def __init__(self) -> None:

        self.filename = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "config/noozy.ini")

        self.config = configparser.ConfigParser()
        # print("reading config file : " + self.filename)
        # print(os.path.exists(self.filename))
        self.config.read(self.filename)

        # print("lalala")
        # print(self.config["RESULT_REDIS"])
        self.host = self.config["RESULT_REDIS"]["Host"]
        self.port = self.config["RESULT_REDIS"]["Port"]
        self.password = self.config["RESULT_REDIS"]["Password"]

        logging.debug(self.host)

        try:
            if not self.password:
                self.client = Client(host=self.host, port=self.port, decode_responses=True)
            else:
                self.client = Client(host=self.host, port=self.port, password=self.password, decode_responses=True)
                self.client.ping()
                print("voila redis4engine connected")
        except Exception as e:
            logging.error(f"ERREUR : Impossible de créer un client REDIS: {str(e)}")
            raise

    def put_item(self, user_id=None, algorithm_id=None, item=None) -> None:
        '''
        get the list of (id,datetime)
        :param date : the oldest available item (based on dc:available date field)
        :param parameters: if None, will only return dc:identifier
        :returns metadata
        '''
        logging.info(f'put - {user_id} - {algorithm_id}...')

        ## rejson api - having issues
        ## https://github.com/RedisJSON/redisjson-py/blob/master/API.md
        # self.client.jsonset(user_id, path="." + algorithm_id, obj=item)
        # self.client.jsonget(user_id, path="." + algorithm_id)
        # self.client.jsondel(user_id, path="." + algorithm_id)
        # self.client.jsonset(user_id, path=Path.rootPath(), obj={})
        # self.client.jsonset(user_id, path="." + algorithm_id, obj=None)
        # self.client.jsonobjlen(user_id, path="." + algorithm_id)
        # self.client.jsonobjkeys(user_id, path="." + algorithm_id)
        # self.client.jsondel(user_id, path="." + algorithm_id)
        algorithm_id = "." + algorithm_id

        if len(self.client.keys(user_id)) > 0:
            try:
                self.client.execute_command('JSON.SET', user_id, algorithm_id, json.dumps(item))
                logging.info(f'added: {user_id} - {algorithm_id}')
            except Exception as e:
                logging.warning(f'set failed: {user_id}')
                logging.warning(f'message: {str(e)}')
        else:
            try:
                self.client.jsonset(user_id, path=Path.rootPath(), obj={})
                self.client.execute_command('JSON.SET', user_id, algorithm_id, json.dumps(item))
                logging.info(f'added: {user_id} - {algorithm_id}')
            except Exception as e:
                logging.warning(f'set failed: {user_id}')
                logging.warning(f'message: {str(e)}')


def get_item(self, user_id=None):
    try:
        return self.client.jsonget(name=user_id)
    except Exception as e:
        logging.warning(f'get failed: {user_id}')
        logging.warning(f'message: {str(e)}')
