This **Apache Kafka IIoT Lab** is the enterprise-grade conclusion to your messaging protocol series. It demonstrates a distributed event-streaming architecture designed for high throughput and fault tolerance.

***

# 🐘 Apache Kafka IIoT Data Pipeline

A professional-grade simulation environment demonstrating **Apache Kafka (KRaft mode)** as a distributed event store. This stack ingest high-frequency sensor data into **TimescaleDB** for long-term analytics and **Grafana** for real-time visualization.



---

## 🏗️ Architecture Components

1.  **Kafka (KRaft Mode):** The modern, ZooKeeper-less distribution of Apache Kafka handling high-frequency event streams.
2.  **Kafka-UI:** A web-based management console for inspecting topics, consumers, and message payloads.
3.  **TimescaleDB:** Our persistent "Historian" database, optimized for time-series data using Hypertables.
4.  **Kafka Logic App:**
    * **The Producer:** Generates industrial telemetry (JSON) and flushes it to the `factory_telemetry` topic.
    * **The Consumer:** Joins a `db-ingest-group` to poll messages and persist them into the database.
5.  **Grafana:** Visualizes the telemetry stream directly from the database.

---

## 📂 Project Structure

```text
KAFKA_PLAYGROUND/
├── database/
│   └── init-db.sql          # SQL Schema & Hypertable setup
├── scripts/
│   ├── Dockerfile           # Builds Python + librdkafka environment
│   ├── requirements.txt     # confluent-kafka & psycopg2
│   └── kafka_app.py         # Multi-threaded Producer/Consumer script
├── Makefile                 # Simplified dev workflow
└── docker-compose.yml       # Orchestrates the Kafka cluster & DB
```

---

## 🚀 Deployment Guide

### 1. Spin up the Cluster
Execute the one-command setup to build the logic app and launch the services:
```bash
make build
```

### 2. Monitor the Management UI
Kafka can be complex to visualize via CLI. Access the Web UI to see your topics in real-time:
* **Kafka UI:** `http://localhost:8080`
* **Grafana:** `http://localhost:3000` (Admin/Admin)

### 3. Verify Data Persistence
Check the Python logs to ensure the Consumer is successfully writing to the database:
```bash
make logs
```
To effectively visualize your **Apache Kafka** data in **Grafana**, you need to connect to **TimescaleDB** as your data source. Since you are using a hypertable, Grafana can handle the time-series visualization efficiently using standard SQL with some Grafana-specific macros.

### 1. Add the Data Source
1.  Open Grafana at `http://localhost:3000`.
2.  Go to **Connections** > **Data Sources** > **Add data source**.
3.  Select **PostgreSQL**.
4.  Configure the settings:
    * **Host:** `timescaledb:5432`
    * **Database:** `postgres`
    * **User:** `postgres`
    * **Password:** `password`
    * **TLS Mode:** `disable`
    * **Version:** `15` (Matches your docker image)
    * **TimescaleDB:** Set to **Enabled** (This is crucial for performance).

---

### 2. The Time-Series Query
When you create a new **Time series** panel, use the following SQL. This query uses the `$__timeFilter` macro to ensure Grafana only pulls data for the time range selected in the dashboard picker.

```sql
SELECT
  time_bucket('$__interval', time) AS "time",
  topic AS "metric",
  avg(value) AS "Temperature"
FROM kafka_data
WHERE
  time >= $__timeFrom() AND time <= $__timeTo()
GROUP BY 1, 2
ORDER BY 1
```

---

### 3. Understanding the Macros
To become an expert in Grafana for IoT, you should understand how these macros translate to raw SQL:

* **`$__timeFilter(time)`**: Automatically injects a `WHERE` clause based on your dashboard's time picker (e.g., `time BETWEEN '2026-04-17T10:00:00Z' AND '2026-04-17T11:00:00Z'`).
* **`$__timeGroupAlias(time, $__interval)`**: This is the "magic" of Grafana. It groups your high-frequency Kafka data into buckets (e.g., every 5 seconds or 1 minute) based on how far you are zoomed out, preventing the browser from crashing due to too many data points.
* **`GROUP BY 1, 3`**: Refers to the first column (the grouped time) and the third column (the topic/sensor name).



---

### 4. Advanced: Detecting Anomalies
Since you are using TimescaleDB, you can run advanced analytics directly in the Grafana query. For example, to see the **Moving Average** of your Kafka stream to smooth out noise:

```sql
SELECT
  time,
  avg(value) OVER (ORDER BY time ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) as "Smoothed Temp"
FROM kafka_data
WHERE $__timeFilter(time)
ORDER BY time ASC
```

---

### 5. Final Checklist for your README
Add this snippet to your **README.md** to help others (or your future self) set up the dashboard quickly:

```markdown
### 📊 Grafana Setup Cheat Sheet
1. **Source:** PostgreSQL (`timescaledb:5432`)
2. **Table:** `kafka_data`
3. **Time Column:** `time`
4. **Metric Column:** `value`
5. **Recommended Panel:** Time Series
```

By mastering these queries, you've completed the full "Edge to Insight" pipeline: 
**Hardware Simulation (Python) ➔ Streaming (Kafka) ➔ Storage (TimescaleDB) ➔ Visualization (Grafana).**
---

## 🔬 Expert Concepts: Why Kafka?

Kafka is different from MQTT and NATS because it is a **Pull-based** system with **Log Retention**.

| Feature | MQTT / NATS (Standard) | Apache Kafka |
| :--- | :--- | :--- |
| **Storage** | Ephemeral (unless JS enabled) | Durable (Stored on disk by default) |
| **Data Flow** | Broker "Pushes" to Client | Client "Polls" (Pulls) from Broker |
| **Scaling** | Limited by single node | Scales horizontally via **Partitions** |
| **Replay** | Usually not possible | Can "rewind" and replay old data |



---

## 🛠️ Management Commands

| Command | Purpose |
| :--- | :--- |
| `make build` | Builds images and starts the cluster. |
| `make up` | Starts the containers without rebuilding. |
| `make logs` | Streams the Producer/Consumer logs. |
| `make db-shell` | Connects to the SQL terminal. |
| `make clean` | **Destructive:** Wipes all Kafka topics and DB records. |

---

## 🏁 Final Project Goal
Once this stack is running, try stopping the `kafka-logic` container for 1 minute while keeping `kafka` running. When you restart the logic app, observe how the **Consumer** automatically "catches up" by reading the messages that were stored in the Kafka log while it was away. This is the **durability** that makes Kafka the backbone of modern industrial data platforms.