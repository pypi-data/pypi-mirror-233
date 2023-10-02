import hashlib
import ujson as json

from kafka import KafkaConsumer, KafkaProducer
from loguru import logger
from kafka.errors import KafkaError

from gdshop_proto.settings import KafkaSettings


class Kafka:
    _producer = None

    @property
    def producer(self):
        if not self._producer:
            self._producer = KafkaProducer(
                bootstrap_servers=KafkaSettings().KAFKA_BROKER,
                value_serializer=lambda m: json.dumps(m, sort_keys=True).encode(
                    "utf-8"
                ),
                request_timeout_ms=1000,
            )
        return self._producer

    @classmethod
    def kafka(func):
        def wrap(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return wrap

    def send_message(self, topic, /, data):
        data = json.dumps(data, sort_keys=True).encode("utf-8")
        self.data_md5 = hashlib.md5(data).hexdigest()
        future = self.producer.send(topic, {"data_md5": self.data_md5, **self.data})
        try:
            future.get(timeout=10)
        except KafkaError as e:
            logger.exception(e)

    def consume(self, f):
        consumer = KafkaConsumer(
            group_id=KafkaSettings().KAFKA_GROUP,
            bootstrap_servers=KafkaSettings().KAFKA_BROKER,
            auto_offset_reset='earliest',
            consumer_timeout_ms=1000
        )
        consumer.subscribe(topics=KafkaSettings().KAFKA_TOPICS.split(','))

        try:
            while True:
                f(consumer)

        finally:
            consumer.close()
