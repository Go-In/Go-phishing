import certstream
import tldextract
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue = 'domain')
channel.queue_declare(queue = 'extracted_domain')

def print_callback(message, context):
    domain = message['data']['leaf_cert']['all_domains'][0]
    
    extracted_domain = tldextract.extract(domain).domain

    channel.basic_publish(exchange = '',
                          routing_key = 'domain',
                          body = domain)

    channel.basic_publish(exchange = '',
                          routing_key = 'extracted_domain',
                          body = extracted_domain)

try:
    certstream.listen_for_events(print_callback, 'wss://certstream.calidog.io')

finally:
    connection.close()
