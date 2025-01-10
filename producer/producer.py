from kafka import KafkaProducer
from typing import Dict, Any
import json
import time
import os
import random

def create_producer() -> KafkaProducer:
    """Create a Kafka producer with default settings."""
    return KafkaProducer(
        bootstrap_servers=[os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8')
    )


def send_message(producer: KafkaProducer, topic: str, key: str, message: Dict[str, Any]) -> None:
    """Send a message to a Kafka topic."""
    try:
        # Send with key for partition assignment
        future = producer.send(topic, key=key, value=message)
        # get(timeout) returns metadata about the record: partition and offset
        metadata = future.get(timeout=5)
        print(f"Message sent - Key: {key}, Partition: {metadata.partition}, Offset: {metadata.offset}")
    except Exception as e:
        print(f"Error sending message: {repr(e)}")

if __name__ == "__main__":
    producer = create_producer()
    topic = "test_topic"
    i = 0

    unique_ids = ['id1', 'id2', 'id3', 'id4']
    message_counts = {uid: 0 for uid in unique_ids}
    try:
        while True:
            key = random.choice(unique_ids)
            message_counts[key] += 1
            message = {
                'unique_id' : key,
                "message_count": message_counts[key],
                "timestamp": time.time(),
                "message": f"Test message {i}"
            }
            send_message(producer, topic, key, message)
            i += 1
            time.sleep(1)
    finally:
        producer.close()


        