import json
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

# Configuration
conf = {
    'bootstrap.servers': '127.0.0.1:9092',
    'client.id': 'python-producer'
}

producer = Producer(conf)
topic = "test-topic"

def send_data(data):
    # Trigger any available delivery report callbacks from previous produce calls
    producer.poll(0)
    
    # Asynchronously produce a message
    producer.produce(
        topic, 
        json.dumps(data).encode('utf-8'), 
        callback=delivery_report
    )
    
    # Wait for any outstanding messages to be delivered
    producer.flush()

if __name__ == "__main__":
    sample_data = {"status": "success", "message": "Hello from Python!", "id": 101}
    print(f"Sending: {sample_data}")
    send_data(sample_data)