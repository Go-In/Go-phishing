import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue = 'domain_queue')

def callback(ch, method, properties, body):
    print('receive: ' + body.decode('utf-8'))

channel.basic_consume(callback, queue = 'domain_queue', no_ack = True)

channel.start_consuming()
