import pika, json

params = pika.URLParameters('amqps://ddxiysqt:obB1i3fVkIEwbJXYpUCHCVsAZ_66Bg35@rat.rmq2.cloudamqp.com/ddxiysqt')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(body):
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body))