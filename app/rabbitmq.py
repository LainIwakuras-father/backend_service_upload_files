import json

import pika


class RabbitMQ:
    def __init__(self, host="localhost"):
        self.host = host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()

    def send_message(self, queue_name, message):
        self.channel.queue_declare(queue=queue_name, durable=True)

        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close(self):
        self.connection.close()


rabbitmq_client = RabbitMQ()
