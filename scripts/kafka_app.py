import os
import time
import json
import random
import psycopg2
from datetime import datetime
from confluent_kafka import Producer, Consumer, KafkaError
from threading import Thread

# Config
KAFKA_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
DB_URL = "host=timescaledb dbname=postgres user=postgres password=password"
TOPIC = "factory_telemetry"

def get_db_connection():
    while True:
        try:
            return psycopg2.connect(DB_URL)
        except:
            print("Kafka App: Waiting for DB...")
            time.sleep(2)

def kafka_producer():
    """Simulates a sensor sending data to Kafka."""
    p = Producer({'bootstrap.servers': KAFKA_SERVERS})
    print("Producer Started.")
    while True:
        data = {"temp": round(random.uniform(20, 35), 2), "ts": str(datetime.now())}
        p.produce(TOPIC, json.dumps(data).encode('utf-8'))
        p.flush()
        time.sleep(5)

def kafka_consumer():
    """Reads from Kafka and writes to TimescaleDB."""
    c = Consumer({
        'bootstrap.servers': KAFKA_SERVERS,
        'group.id': 'db-ingest-group',
        'auto.offset.reset': 'earliest'
    })
    c.subscribe([TOPIC])
    print("Consumer Started.")
    
    while True:
        msg = c.poll(1.0)
        if msg is None: continue
        if msg.error():
            print(f"Consumer Error: {msg.error()}")
            continue

        data = json.loads(msg.value().decode('utf-8'))
        try:
            conn = get_db_connection()
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
    "INSERT INTO kafka_data (time, topic, value) VALUES (now(), %s, %s)", 
    (TOPIC, data['temp'])
)
            conn.close()
            print(f"[Kafka -> DB] Saved Temp: {data['temp']}")
        except Exception as e:
            print(f"DB Error: {e}")

if __name__ == '__main__':
    # Run Producer in background, Consumer in foreground
    Thread(target=kafka_producer).start()
    kafka_consumer()