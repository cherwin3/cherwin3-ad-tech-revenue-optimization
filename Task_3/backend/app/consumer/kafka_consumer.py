import json
import os
from datetime import datetime
from pathlib import Path

from clickhouse_driver import Client
from dotenv import load_dotenv
from kafka import KafkaConsumer


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

KAFKA_SERVER = os.getenv(
    "KAFKA_SERVER",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "ad-events"
)

CLICKHOUSE_HOST = os.getenv(
    "CLICKHOUSE_HOST",
    "localhost"
)

CLICKHOUSE_PORT = int(
    os.getenv("CLICKHOUSE_PORT", "9000")
)

CLICKHOUSE_USER = os.getenv(
    "CLICKHOUSE_USER",
    "adstream"
)

CLICKHOUSE_PASSWORD = os.getenv(
    "CLICKHOUSE_PASSWORD",
    "adstream123"
)

CLICKHOUSE_DATABASE = os.getenv(
    "CLICKHOUSE_DATABASE",
    "adstream"
)


def create_clickhouse_client() -> Client:
    client = Client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        user=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE
    )

    client.execute("SELECT 1")

    print("Connected to ClickHouse successfully")

    return client


def create_kafka_consumer() -> KafkaConsumer:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="adstream-clickhouse-consumer",
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        )
    )

    print("Connected to Kafka successfully")

    return consumer


def convert_timestamp(timestamp_value: str) -> datetime:
    if not timestamp_value:
        return datetime.utcnow()

    normalized_timestamp = timestamp_value.replace(
        "Z",
        "+00:00"
    )

    parsed_timestamp = datetime.fromisoformat(
        normalized_timestamp
    )

    return parsed_timestamp.replace(tzinfo=None)


def insert_event(
    clickhouse_client: Client,
    event: dict
) -> None:

    event_time = convert_timestamp(
        event.get("timestamp", "")
    )

    clickhouse_client.execute(
        """
        INSERT INTO ad_events
        (
            user_id,
            page_id,
            recommended_position,
            ad_format,
            predicted_viewability,
            estimated_rpm,
            source,
            llm_used,
            latency_ms,
            event_time
        )
        VALUES
        """,
        [
            (
                str(event.get("user_id", "")),
                str(event.get("page_id", "")),
                str(
                    event.get(
                        "recommended_position",
                        ""
                    )
                ),
                str(event.get("ad_format", "")),
                float(
                    event.get(
                        "predicted_viewability",
                        0
                    )
                ),
                float(event.get("estimated_rpm", 0)),
                str(event.get("source", "")),
                int(bool(event.get("llm_used", False))),
                float(event.get("latency_ms", 0)),
                event_time
            )
        ]
    )


def run_consumer() -> None:
    try:
        clickhouse_client = create_clickhouse_client()
        kafka_consumer = create_kafka_consumer()

        print(
            "Kafka consumer started. "
            "Waiting for ad events..."
        )

        for message in kafka_consumer:
            try:
                event = message.value

                print("Kafka event received:", event)

                insert_event(
                    clickhouse_client,
                    event
                )

                print(
                    "Event stored successfully "
                    "in ClickHouse"
                )

            except Exception as event_error:
                print(
                    "Failed to process event:",
                    event_error
                )

    except KeyboardInterrupt:
        print("Kafka consumer stopped")

    except Exception as error:
        print("Consumer startup error:", error)


if __name__ == "__main__":
    run_consumer()