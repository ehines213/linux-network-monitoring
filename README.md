# Linux Network Monitoring Platform

A lightweight Linux-based monitoring platform designed to collect and store host-level system and network metrics using a local agent and a FastAPI backend. This project demonstrates practical systems administration concepts including service management, security hardening, and agent-based telemetry collection.

---

## Overview

The platform consists of two primary components:

1. **Monitoring API**
   - FastAPI application responsible for receiving, validating, and storing metrics
   - Exposes endpoints for health checks and querying recent metrics
   - Stores data locally using SQLite

2. **Monitoring Agent**
   - Python-based collector running on the host
   - Periodically gathers system and network metrics
   - Sends metrics to the API over HTTP using an authenticated request

Both components are managed using `systemd` and configured to run as non-root services with security hardening applied.

---

## Architecture

Linux Host
├── linux-netmon-agent.service
│ └── agent.py
│ └── POST /ingest (authenticated)
│
└── linux-netmon-api.service
└── FastAPI (Uvicorn)
├── GET /health
├── GET /latest
└── SQLite (metrics.db)

---
## Project Structure

linux-network-monitoring/
├── agent/
│ ├── agent.py
│ └── .venv/
├── server/
│ ├── app.py
│ ├── metrics.db
│ ├── static/
│ └── .venv/
├── systemd/
│ ├── linux-netmon-api.service
│ └── linux-netmon-agent.service
├── .gitignore
└── README.md

---
## Metrics Collected

The agent collects and transmits the following metrics:

- CPU utilization percentage
- Memory utilization percentage
- Disk utilization percentage
- Network receive throughput (kbps)
- Network transmit throughput (kbps)
- ICMP ping latency (milliseconds)

Each metric sample is timestamped and associated with the host name.

---

## API Authentication

Metric ingestion requires an API key supplied via HTTP header:

X-API-KEY:<key>

The API key is read from an environment variable at runtime:

NETMON_API_KEY=change_me


Requests without a valid key are rejected with HTTP 401.

---

## API Endpoints

### Health Check
GET /health

Returns a simple status response indicating the API is running.

### Latest Metrics
GET /latest?limit=<n>

Returns the most recent metric entries, ordered by ingestion time.

### Metric Ingestion
POST /ingest

Accepts a JSON payload containing host metrics. Requires a valid API key.

## systemd Integration

Both the API and agent are managed using systemd service units.

### API Service

Runs FastAPI using Uvicorn
Bound to localhost (127.0.0.1)
Uses a Python virtual environment
Automatically restarts on failure

### Agent Service

Executes the monitoring agent on a fixed interval
Sends metrics to the local API
Runs as an unprivileged user
Restarted automatically on failure

## Security Hardening

The systemd services apply multiple hardening directives, including:
No privilege escalation (NoNewPrivileges)
Restricted filesystem access (ProtectSystem, ProtectHome)
Isolated temporary directories (PrivateTmp)
Explicit write access limited to the project directory
Non-root execution
Secrets are not stored in source code and are injected via environment variables.

## Usage Examples

Health check:

curl http://127.0.0.1:8000/health


Query recent metrics:

curl "http://127.0.0.1:8000/latest?limit=5"

## Future Enhancements

TLS termination with a reverse proxy
Centralized logging and alerting
Prometheus-compatible metrics endpoint
Multi-host agent deployment
Role-based authentication
Visualization dashboard integration



