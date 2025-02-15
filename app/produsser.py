import json

from pika import BlockingConnection, ConnectionParameters

connection_params = ConnectionParameters(
    host="localhost",
    port=5672
)

class RabbitMQ:
    def __init__(self, host="localhost"):
        self.host = host
        self.connection = BlockingConnection(connection_params)
        self.channel = self.connection.channel()

    def send_message(self, queue_name, message):
        self.channel.queue_declare(queue=queue_name, durable=True)

        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
        )

    def close(self):
        self.connection.close()


rabbitmq_client = RabbitMQ()
