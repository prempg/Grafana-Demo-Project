# Grafana-Demo-Project
Collecting logs and built the Dashboard.
# Server Log Monitoring Dashboard (Grafana + Loki)

A simple and practical demo project that collects, stores, and visualizes web server access logs in real time using **Docker**, **Grafana**, **Loki**, and **Python**.

---

## What This Project Does

1. **Python Script (`log_pusher.py`):** Generates realistic web server logs (IP address, endpoints, HTTP status codes like 200, 404, 500) and sends them to Loki.
2. **Grafana Loki:** Receives the logs, indexes them by labels, and stores them efficiently.
3. **Grafana Dashboard:** Displays the logs visually through live charts, error counters, and status code distributions.

---

## Tech Stack

* **Docker & Docker Compose** (Container setup)
* **Grafana** (Visualization dashboard)
* **Grafana Loki** (Log storage engine)
* **Python 3** (Log generator script)

---

## Project Structure

```text
├── docker-compose.yml   # Starts Grafana and Loki containers
├── loki-config.yaml     # Basic Loki setup configuration
├── log_pusher.py        # Python script to stream logs
└── README.md            # Project guide

How to Run Locally
1. Start Grafana and Loki
Open terminal inside this project folder and run:

docker compose up -d

Grafana URL: http://localhost:3000 (Username: admin, Password: admin)

Loki Status: http://localhost:3100/ready (Should show ready)

Connect Loki to Grafana
Open Grafana in your browser (http://localhost:3000).

Go to Connections > Data Sources > Add data source.

Choose Loki.

In the URL field, enter: http://loki:3100

Click Save & Test.

3. Start Streaming Logs
Run the Python script in your terminal to send continuous logs:

Bash
python log_pusher.py
Dashboard Panels & LogQL Queries
Live Server Logs (Logs Panel):

Code snippet
{job="web_server_access_logs"}
Requests Per Second (Time Series):

Code snippet
sum(rate({job="web_server_access_logs"}[1m]))
500 Internal Server Errors (Alert/Stat Panel):

Code snippet
sum(rate({job="web_server_access_logs"} |= "500" [1m]))
Status Code Distribution (Pie Chart):

Code snippet
sum by (status) (
  count_over_time(
    {job="web_server_access_logs"}
    | pattern `<ip> - - [<time>] "<method> <endpoint> <proto>" <status> <bytes> rt=<rt>ms`
    [5m]
  )
)
What I Learned from This Demo
Running multi-container monitoring stacks using Docker Compose.

Structuring and pushing custom log streams to Loki via HTTP API.

Using LogQL pattern matching to extract fields dynamically without writing complex regex.

Designing real-time observability dashboards for server health tracking.
