from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_DSB: str
    SCHEMA: str = "public"


class KafkaSettings(BaseSettings):
    KAFKA_BROKER: str
    KAFKA_GROUP: str = "default"
