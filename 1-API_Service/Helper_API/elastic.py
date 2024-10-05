from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from Helper_API.loghandler import logger
import logging
import os 


load_dotenv('.env')

class ElasticConnection():
    es_client = Elasticsearch(os.getenv('ELASTIC_SEARCH_URL'))

    async def checkElasticsearchConnection(self):
        try:
            is_connected = False
            while not is_connected:
                if not self.es_client.ping():
                    logging.error(f"Elasticsearch Server is Down")
                response = self.es_client.cluster.health()
                logger.info(f"ElasticSearch Server is up and status is: {response}")
                is_connected = True
        except Exception as err:
            logging.error(f"Error while Connecting to ElasticSearch Server: {err}")


elastic_connection = ElasticConnection()