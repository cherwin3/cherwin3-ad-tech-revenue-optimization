import json
import os
from typing import Any, Dict, Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError


KAFKA_SERVER = os.getenv(
    "KAFKA_SERVER",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "ad-events"
)

producer: Optional[KafkaProducer] = None


def get_producer() -> KafkaProducer:
    global producer

    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda value: json.dumps(
                value
            ).encode("utf-8"),
            request_timeout_ms=5000
        )

        print(
            f"Kafka producer connected to {KAFKA_SERVER}"
        )

    return producer


def publish_ad_event(event: Dict[str, Any]) -> bool:
    try:
        kafka_producer = get_producer()

        future = kafka_producer.send(
            KAFKA_TOPIC,
            value=event
        )

        # Wait until Kafka confirms the message
        record_metadata = future.get(timeout=10)

        kafka_producer.flush()

        print(
            "Kafka event published successfully:",
            f"topic={record_metadata.topic},",
            f"partition={record_metadata.partition},",
            f"offset={record_metadata.offset}"
        )

        return True

    except KafkaError as error:
        print(f"Kafka error: {error}")
        return False

    except Exception as error:
        print(f"Kafka publishing error: {error}")
        return False


def close_producer() -> None:
    global producer

    if producer is not None:
        producer.flush()
        producer.close()
        producer = None

        print("Kafka producer closed")