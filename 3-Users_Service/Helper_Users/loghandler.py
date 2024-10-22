import logging
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import datetime
import json
import os 

load_dotenv('.env')


class ElasticLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.client = Elasticsearch(os.getenv('ELASTIC_SEARCH_URL'))


    def emit(self, record):
        document = {
            "Message": record.msg,
            "Service": record.name,
            "Level": record.levelname,
            "TimeStamp": datetime.datetime.now().isoformat()
        }
        json_document = json.dumps(document)
        self.client.index(index="users_service", document=json_document)


elastic_handler = ElasticLogHandler()
logger = logging.getLogger('Users_Service')
logger.setLevel(logging.INFO)
logger.addHandler(elastic_handler)

