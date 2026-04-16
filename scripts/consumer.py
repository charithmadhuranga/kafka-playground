from confluent_kafka import Consumer, KafkaError

# Configuration
conf = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest' # Start from the beginning if no offset exists
}

consumer = Consumer(conf)
topic = "test-topic"
consumer.subscribe([topic])

print(f"Listening for messages on topic: {topic}...")

try:
    while True:
        msg = consumer.poll(1.0) # Timeout in seconds

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break

        print(f"📩 Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()