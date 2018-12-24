import pika
import logging
import tldextract
from pyvirtualdisplay import Display
from urllib import request
from selenium import webdriver

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

logging.info('Connecting to message broker')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

logging.info('Creating exchange and message queue')

channel.exchange_declare(exchange = 'domain', exchange_type = 'fanout')

domain_queue = channel.queue_declare(exclusive = True)

domain_queue_name = domain_queue.method.queue

channel.queue_bind(exchange = 'domain', queue = domain_queue_name)

logging.info('Creating virtual display')

display = Display(visible = 0, size = (1280, 720))
display.start()

logging.info('Creating webdriver')

browser = webdriver.Firefox()

browser.set_page_load_timeout(10)

def callback(ch, method, properties, body):
    log_domain = body.decode('utf-8')

    logging.info('Got {}'.format(log_domain))

    extracted_tld = tldextract.extract(log_domain)

    try:
        logging.info('{}'.format(extracted_tld.domain + '.' + extracted_tld.suffix))

        browser.get('https://' + extracted_tld.domain + '.' + extracted_tld.suffix)

        screenshot = browser.save_screenshot('../screenshot/' + extracted_tld.domain + '.png')
    except Exception as e:
        logging.info('{}: {}'.format(log_domain, str(e)))
        

channel.basic_consume(callback, queue = domain_queue_name, no_ack = True)

try:
    logging.info('Starting page capturer')

    channel.start_consuming()

finally:
    logging.info('Closing webdriver and message broker connection')

    browser.quit()

    connection.close()
