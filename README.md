Overview

This project is a Linux-based network and system monitoring platform designed to provide visibility into system health and basic network connectivity. It uses a lightweight Python agent to collect metrics and exposes them through a FastAPI backend for real-time monitoring and historical review. The platform is intended for small environments, labs, or internal IT operations where simplicity, transparency, and reliability are priorities.
Features
Collects system metrics including CPU usage, memory utilization, disk usage, uptime, and hostname
Performs basic network reachability checks (e.g., ping/latency)
Exposes metrics via a REST API built with FastAPI
Uses structured JSON logging for consistency and easy analysis
Runs persistently as a systemd service
Designed for reproducible deployment and clear documentation
Architecture
The platform follows a simple agent-and-API model:
Monitoring Agent
Runs locally on a Linux system
Periodically gathers system and network metrics
Writes structured output to logs or sends data to the API
FastAPI Backend
Provides REST endpoints for viewing current status and collected data
Supports health checks and basic observability
Can be extended for dashboards or alerting
This design keeps the system lightweight while remaining extensible for future features.
Technologies Used
Linux
Python 3
FastAPI
systemd
JSON-based logging
Basic networking utilities (ping, routing awareness)
Installation and Setup (High-Level)
Clone the repository to a Linux system.
Install Python dependencies using pip.
Configure the monitoring agent settings as needed.
Enable and start the systemd service to run the agent persistently.
Launch the FastAPI backend and verify API access.
Detailed setup steps and configuration examples are included in the repository files.
Use Cases
Monitoring Linux servers or workstations in small environments
Supporting internal IT operations with quick visibility into system health
Learning and demonstrating Linux monitoring, automation, and service management
Serving as a foundation for more advanced observability or alerting systems
Future Enhancements
Alerting and threshold-based notifications
Authentication and access control for API endpoints
Historical data storage and visualization
Multi-host aggregation support
