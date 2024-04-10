import pika, json
from django.core.management.base import BaseCommand
from auth_api.models import Search, Keyword, Url
from django.contrib.auth.models import User



class Command(BaseCommand):
    help='Starts the rabbit mq consumer'

    def handle(self, *args, **kwargs):
        params = pika.URLParameters('amqps://ddxiysqt:obB1i3fVkIEwbJXYpUCHCVsAZ_66Bg35@rat.rmq2.cloudamqp.com/ddxiysqt')

        connection = pika.BlockingConnection(params)

        channel = connection.channel()

        channel.queue_declare(queue='main')

        def callback(ch, method, properties, body):
            print('Received in django')
            data = json.loads(body)
            user_instance = User.objects.get(id=data['userId'])
            search = Search.objects.create(name=data['name'], created_by=user_instance,result_id=data['result_id'])
            urls_instances =[Url(domain_name=url,search_id=search ) for url in data['urls']]
            Url.objects.bulk_create(urls_instances)
            if 'keyword' in data:
                Keyword.objects.create(word=data['keyword'], search_id=search)

        channel.basic_consume(queue='main',on_message_callback=callback,auto_ack=True)
        print ('Started consuming')
        channel.start_consuming()

        channel.close()