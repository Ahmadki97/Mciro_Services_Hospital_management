from Helper_Users.loghandler import logger
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import logging
import os 


load_dotenv('.env')

async def checkElasticConnection():
    try:
        client = Elasticsearch(os.getenv('ELASTIC_SEARCH_URL'))
        is_connected = False
        while not is_connected:
            if client.ping():
                logger.info(f"Elasticsearch Server is up and Running")
                response = client.cluster.health()
                logger.info(f"Elasticsearch Cluster Status is: {response}")
                is_connected = True
            else:
                logging.error(f"Elasticsearch Server is Down")
    except Exception as err:
        logging.error(f"Elasticsearch connection failed: {err}")