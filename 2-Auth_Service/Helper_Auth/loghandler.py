from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import datetime
import logging
import json
import os 


load_dotenv('.env')

es_client = Elasticsearch(os.getenv('ELASTIC_SEARCH_URL'))

class ElasticSearchHandler(logging.Handler):
    def __init__(self, es_client):
        super().__init__()
        self.es_client = es_client
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.json_documents = []


    def emit(self, record):
        document = {
            "Message": record.msg,
            "LevelName": record.levelname,
            "Service": record.name,
            "TimeStamp": datetime.datetime.utcnow().isoformat(),  
        }
        json_doc = json.dumps(document)
        self.es_client.index(index="auth_service", document=json_doc)


handler = ElasticSearchHandler(es_client)
logger = logging.getLogger('Auth_Service')
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
