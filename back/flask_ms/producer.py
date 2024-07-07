import pika, json

params = pika.URLParameters('amqps://ddxiysqt:obB1i3fVkIEwbJXYpUCHCVsAZ_66Bg35@rat.rmq2.cloudamqp.com/ddxiysqt')

class RabbitMQPublisher:
    def __init__(self):
        self.params = params
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(self.params)
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPError as err:
            print(f"Error connecting to RabbitMQ: {err}")

    def publish(self, body):
        if not self.connection or self.connection.is_closed or not self.channel or self.channel.is_closed:
            self.connect()
        
        try:
            self.channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body))
        except pika.exceptions.AMQPError as err:
            print(f"Error publishing message: {err}")
            self.connect()