import pika
import logging

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

try:
    logging.info('Reading target domain list')

    target_domain_file = open('../data/target_domain.txt', 'r')

    target_domain_list = target_domain_file.readlines()
finally:
    logging.info('Closing target domain list')

    target_domain_file.close()

logging.info('Connecting to message queue broker')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

logging.info('Creating message queue')

channel.queue_declare(queue = 'domain')

def callback(ch, method, properties, body):
    logging.info('Got {}'.format(body.decode('utf-8')))

channel.basic_consume(callback, queue = 'domain', no_ack = True)

logging.info('Starting domain name scorer')

channel.start_consuming()
