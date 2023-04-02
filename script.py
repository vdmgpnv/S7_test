from services.amqp.producer import RabbitProducer

body = {"filename": "20230211_123_DME.csv"}

if __name__ == '__main__':
    with RabbitProducer("files") as producer:
        producer.send_message(body)