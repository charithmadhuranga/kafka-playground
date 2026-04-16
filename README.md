

-----

# 🚀 Kafka KRaft & Kafka UI Lab

This laboratory provides a modern, Zookeeper-less setup for Apache Kafka using **KRaft mode**. It includes **Kafka UI** for visual cluster management and Python scripts for basic Producer/Consumer testing.

## 🛠️ Prerequisites

  - **Docker & Docker Compose** installed.
  - **Python 3.8+** (for testing scripts).
  - `confluent-kafka` Python library:
    ```bash
    pip install confluent-kafka
    ```

## 🏗️ Architecture

The setup utilizes a **Dual-Listener** configuration to solve the common "Docker Networking" conflict where external scripts cannot find the broker.

  - **INTERNAL (29092):** Used by Kafka UI and other containerized services to communicate within the Docker network.
  - **EXTERNAL (9092):** Used by your host machine (IDE, CLI, Python scripts) to connect to the broker.

-----

## 🚀 Getting Started

### 1\. The Docker Compose File

Create a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'

services:
  kafka:
    image: apache/kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: 'broker,controller'
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka:9093'
      KAFKA_LISTENERS: 'INTERNAL://0.0.0.0:29092,EXTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093'
      KAFKA_ADVERTISED_LISTENERS: 'INTERNAL://kafka:29092,EXTERNAL://localhost:9092'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT'
      KAFKA_INTER_BROKER_LISTENER_NAME: 'INTERNAL'
      KAFKA_CONTROLLER_LISTENER_NAMES: 'CONTROLLER'
      CLUSTER_ID: 'MkU3OEVBNTcwNTJENDM2Qk'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    ports:
      - "8080:8080"
    depends_on:
      - kafka
    environment:
      KAFKA_CLUSTERS_0_NAME: local-kraft
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:29092
      DYNAMIC_CONFIG_ENABLED: 'true'
```

### 2\. Start the Cluster

Run the following command. The `-v` flag ensures a clean state by removing any old metadata volumes.

```bash
docker-compose down -v && docker-compose up -d
```

### 3\. Access the Dashboard

Open your browser to: **[http://localhost:8080](https://www.google.com/search?q=http://localhost:8080)**

-----

## 🐍 Testing with Python

### `producer.py`

```python
import json
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': '127.0.0.1:9092',  # Using the EXTERNAL listener
    'client.id': 'python-producer'
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}]")

sample_data = {"status": "success", "message": "Hello from Python!", "id": 101}
producer.produce("test-topic", json.dumps(sample_data).encode('utf-8'), callback=delivery_report)
producer.flush()
```

### `consumer.py`

```python
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(["test-topic"])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        print(f"📩 Received: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
```

-----

## 📝 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **Connection Refused** | Ensure `ports: - "9092:9092"` is in your YAML. |
| **No such host is known** | In Python, use `127.0.0.1:9092`, not `kafka:9092`. |
| **Metadata Conflict** | Run `docker-compose down -v` to wipe the KRaft state. |