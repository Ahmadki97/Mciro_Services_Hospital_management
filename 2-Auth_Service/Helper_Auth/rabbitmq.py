import pika 
import os 
from Helper_Auth.loghandler import logger
from dotenv import load_dotenv


load_dotenv('.env')

async def checkRabbitMQConnection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        logger.info(f"CheckRabbitMQConnection() Method, Auth Service Connected to RabbitMQ Server")
        connection.close()
    except Exception as err:
        logger.error(f"Error in checkRabbitMQConnection() Method: {err}")


async def startPuplishingMessage(queue, exchange_name, routing_key, body):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body)
        logger.info(f"startPuplishingMessage() Method, New Message Published to RabbitMQ Server queue name is  {queue}")
    except Exception as err:
        logger.error(f"Error in startPuplishingMessage() Method: {err}")