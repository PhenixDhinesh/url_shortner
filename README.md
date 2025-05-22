# Advanced URL Shortener

## Project Overview

This project is building a robust, scalable, and observable URL shortening service using a **multi-service architecture** orchestrated by **Docker Compose**. Beyond basic URL shortening and redirection, our core motive is to demonstrate an **event-driven design** for analytics processing and integrate a comprehensive **observability stack** for logging and monitoring.

This setup showcases advanced Docker Compose features, service orchestration, and best practices for building distributed systems.

---

## Key Features

* **URL Shortening & Redirection**: Core functionality to convert long URLs into short, memorable codes and redirect users.
* **Event-Driven Analytics**: Decoupled processing of URL visit and shortening events via a message queue.
* **Centralized Logging**: Aggregation of logs from all services for easy debugging and analysis.
* **Comprehensive Observability**: Integration of tools for monitoring application health and performance.

---

## Project Structure

The project is divided into several key services and components:

* **`backend/`**: The Flask API service handling URL shortening, redirection, and interaction with the database and message queue. This includes database models, migrations, and core business logic.
    * **Refer to `backend/README.md` for detailed setup and usage instructions.**
* **`frontend/`** (Planned): A static web interface for users to shorten URLs and view basic stats.
* **`analytics-worker/`** (Planned): A separate worker service consuming events from the message queue and processing them for analytics.
* **Data Stores** (Planned): Integration of PostgreSQL for persistent storage and Redis for caching.
* **Message Broker** (Planned): RabbitMQ to facilitate event-driven communication.
* **Observability Stack** (Planned): Elasticsearch, Kibana, and Filebeat for centralized logging and analytics visualization.
* **`docker-compose.yml`** (Planned): The orchestrator to bring all services together for local development and deployment.

---

## Getting Started

To begin working with any specific part of the project, navigate to its respective directory (e.g., `backend/`) and consult its dedicated `README.md` file for detailed setup, installation, and running instructions.