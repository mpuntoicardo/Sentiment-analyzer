import pika

params = pika.URLParameters('amqps://ddxiysqt:obB1i3fVkIEwbJXYpUCHCVsAZ_66Bg35@rat.rmq2.cloudamqp.com/ddxiysqt')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Received in django')
    print(body)

channel.basic_consume(queue='main',on_message_callback=callback,auto_ack=True)
print ('Started consuming')
channel.start_consuming()

channel.close()