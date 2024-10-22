from Helper_Users.loghandler import logger
from Services_Users.doctorservices import createDoctor
from Services_Users.patientservices import createPatient
from database import get_db
from dotenv import load_dotenv
import pika 
import json
import os 


load_dotenv('.env')

connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
channel = connection.channel()

async def checkRabbitmqConnection():
    try:
        if connection:
            logger.info(f"CheckRabbitMQConnection() Method, Users Service Connected to RabbitMQ Server")    
        else:
            logger.error(f"Error in checkRabbitMQConnection() Method, Users Service could not connect to RabbitMQ Server")
    except Exception as err:
        logger.error(f"Error in checkRabbitMQConnection() Method: {err}")


async def startPuplishingMessage(queue: str, exchange_name: str, routing_key: str, body):
    try:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body)
        logger.info(f"startPuplishingMessage() Method, New Message Published to RabbitMQ Server queue name is  {queue}")
    except Exception as err:
        logger.error(f"Error in startPuplishingMessage() Method: {err}")


def startConsumeUserSignupMessage():
    try:
        while True:
            print(f"Hello from startConsumeUserSignupMessage() Function..")
            channel.basic_consume(queue='user-signup', on_message_callback=consumeUsersignupMessage, auto_ack=True)
            logger.info(f"startConsumeUserSignupMessage() Method, Finished Consuming Message Successfully..")
            channel.start_consuming()
    except Exception as err:
        logger.error(f"Error in startConsumeUserSignupMessage() Method: {err}")


def consumeUsersignupMessage(ch, method,properties, body):
    db = next(get_db())
    try:
        message  = json.loads(body)
        print(f"Data in the message: {message}")
        print(f"Hello from startConsumeUsersignupMessage() Consumer")
        if message['user_type'] == 'doctor':
            del message['user_type']
            createDoctor(doctor=message, db=db)
            logger.info(f"consumeUsersignupMessage() Method, Doctor user created successfully.")
        else:
            del message['user_type']
            createPatient(patient=message, db=db)
            logger.info(f"consumeUsersignupMessage() Method, Patient user created successfully.")
            ch.basic_ack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as err:
        logger.error(f"Error in consumeUsersignupMessage() Method: {err}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        