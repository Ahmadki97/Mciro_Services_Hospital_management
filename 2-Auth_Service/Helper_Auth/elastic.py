from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from Helper_Auth.loghandler import logger
import logging
import os 


load_dotenv('.env')


es_client = Elasticsearch(os.getenv('ELASTIC_SEARCH_URL'))

async def checkElasticsearchConnection():
    try:
        print(f"Checking Elasticsearch connection")
        is_connected = False
        while not is_connected:
            print(f"Elasticsearch connection while statement")
            if not es_client.ping():
                print(f"Elasticsearch connection If statement")
                logging.error(f"Elasticsearch Server is Down")
            response = es_client.cluster.health()
            logger.info(f"ElasticSearch Server is up and status is: {response}")
            print(f"Elastic Search is connected")
            is_connected = True
    except Exception as err:
        logging.error(f"Error while Connecting to ElasticSearch Server: {err}")

