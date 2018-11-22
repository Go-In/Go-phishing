import certstream
import tldextract
import pika
import logging

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

logging.info('Connecting to message queue broker')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

logging.info('Creating message queue')

channel.queue_declare(queue = 'domain')
channel.queue_declare(queue = 'extracted_domain')

def callback(message, context):
    domain = message['data']['leaf_cert']['all_domains'][0]
    
    extracted_domain = tldextract.extract(domain).domain

    logging.info('Got {}'.format(domain))

    channel.basic_publish(exchange = '',
                          routing_key = 'domain',
                          body = domain)

    channel.basic_publish(exchange = '',
                          routing_key = 'extracted_domain',
                          body = extracted_domain)

try:
    logging.info('Starting CertStream receiver')

    certstream.listen_for_events(callback, 'wss://certstream.calidog.io')

finally:
    logging.info('Closing message queue connection')

    connection.close()
