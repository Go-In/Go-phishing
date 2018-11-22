import pika
import logging
import random
import json

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

try:
    logging.info('Reading target domain list')

    target_domain_file = open('../data/target_domain.txt', 'r')

    target_domain_list = target_domain_file.read().splitlines()

finally:
    logging.info('Closing target domain list')

    target_domain_file.close()

logging.info('Connecting to message queue broker')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

logging.info('Creating message queue')

channel.queue_declare(queue = 'domain')

channel.queue_declare(queue = 'score')

def callback(ch, method, properties, body):
    log_domain = body.decode('utf-8')

    logging.info('Got {}'.format(log_domain))

    for target_domain in target_domain_list:
        message = {}

        message['type'] = 1
        message['target_domain'] = target_domain
        message['log_domain'] = log_domain
        message['domain_score'] = random.randrange(101)

        channel.basic_publish(exchange = '',
                              routing_key = 'score',
                              body = json.dumps(message))

channel.basic_consume(callback, queue = 'domain', no_ack = True)

try:
    logging.info('Starting domain name scorer')

    channel.start_consuming()

finally:
    logging.info('Closing message queue connection')

    connection.close()
