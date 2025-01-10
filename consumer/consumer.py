from kafka import KafkaConsumer
from typing import Any
import json
import os

def create_consumer(topic: str) -> KafkaConsumer:
    """Create a Kafka consumer with default settings."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=[os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my_consumer_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

if __name__ == "__main__":
    topic = "test_topic"
    consumer = create_consumer(topic)

    try:
        print("Starting consumer... waiting for messages")
        for message in consumer:
            print(f"""
                Topic: {message.topic}
                Partition: {message.partition}
                Offset: {message.offset}
                Key: {message.key}
                Value: {message.value}
            """)
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()