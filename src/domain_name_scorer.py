import pika
import logging
import json
import nltk
import tldextract

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

try:
    logging.info('Reading target domain list')

    target_domain_file = open('../data/target_domain.txt', 'r')

    target_domain_list = target_domain_file.read().splitlines()

finally:
    logging.info('Closing target domain list')

    target_domain_file.close()

logging.info('Connecting to message broker')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

logging.info('Creating exchange and message queue')

channel.exchange_declare(exchange = 'domain', exchange_type = 'fanout')

domain_queue = channel.queue_declare(exclusive = True)

channel.queue_declare(queue = 'score')

domain_queue_name = domain_queue.method.queue

channel.queue_bind(exchange = 'domain', queue = domain_queue_name)

def callback(ch, method, properties, body):
    log_domain = body.decode('utf-8')

    logging.info('Got {}'.format(log_domain))

    for target_domain in target_domain_list:
        message = {}

        extracted_log_domain = tldextract.extract(log_domain).domain
        extracted_target_domain = tldextract.extract(target_domain).domain

        message['type'] = 1
        message['target_domain'] = target_domain
        message['log_domain'] = log_domain
        message['domain_score'] = (1 - (nltk.jaccard_distance(set(extracted_log_domain), set(extracted_target_domain)))) * 100

        logging.info('{}'.format(message['domain_score']))

        channel.basic_publish(exchange = '',
                              routing_key = 'score',
                              body = json.dumps(message))

channel.basic_consume(callback, queue = domain_queue_name, no_ack = True)

try:
    logging.info('Starting domain name scorer')

    channel.start_consuming()

finally:
    logging.info('Closing message broker connection')

    connection.close()
