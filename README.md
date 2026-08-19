<<<<<<< HEAD
 AdStream Revenue Optimization API
Project Overview
AdStream Revenue Optimization API is a FastAPI-based backend system designed to improve advertisement placement performance using user engagement signals such as scroll depth, time on page, device type, and page type.
The system recommends suitable advertisement positions and formats while using Redis caching, Kafka event streaming, ClickHouse analytics storage, security validation, and audit logging.


⸻


Main Objective
The objective of this project is to improve advertisement viewability and revenue performance while reducing API latency and maintaining secure backend processing.
The system focuses on:
Optimizing ad placement
Improving API response time
Reducing repeated computation using Redis
Streaming events through Kafka
Storing analytics data in ClickHouse
Validating incoming requests
Recording user and system activity using audit logs


⸻


Technology Stack
The project uses:
Python
FastAPI
Pydantic
Redis
Apache Kafka
ClickHouse
Docker
Pytest
Gemini LLM integration


⸻


Project Architecture
User Request
     ↓
FastAPI
     ↓
Pydantic Validation
     ↓
Redis Cache Check
     ↓
     ├── Cache Hit
     │      ↓
     │   Cached Response
     │
     └── Cache Miss
            ↓
     Optimization Engine
            ↓
        LLM Service
            ↓
        Redis Cache
            ↓
        API Response
            ↓
       Kafka Producer
            ↓
          Kafka
            ↓
       Kafka Consumer
            ↓
        ClickHouse

FastAPI
   ↓
Audit Logger
   ↓
logs/audit.log


⸻


FastAPI Endpoints
Root Endpoint
GET /
Used to verify that the API is running.
Health Endpoint
GET /health
Example response:
{
  "api": "healthy",
  "redis": "connected"
}
Optimize Advertisement Placement
POST /optimize-placement
Example request:
{
  "user_id": "U101",
  "page_id": "P501",
  "scroll_depth": 65,
  "time_on_page": 45,
  "device_type": "mobile",
  "page_type": "news"
}
The endpoint returns:
Recommended ad position
Ad format
Predicted viewability
Estimated RPM
Reason
Response source
LLM status
Request latency


⸻


Redis Caching
Redis is used to cache repeated optimization requests.
The first request is processed by the optimization engine.
Example:
source = optimization_engine
latency_ms = 977.59
The same request is later returned from Redis.
Example:
source = redis_cache
latency_ms = 1.33
This significantly reduces latency for repeated requests.


⸻


Kafka Integration
Kafka is used for asynchronous event streaming.
After an optimization response is generated, an event is published to Kafka.
The event is received by the Kafka consumer and forwarded to ClickHouse.
Flow:
FastAPI
   ↓
Kafka Producer
   ↓
Kafka
   ↓
Kafka Consumer
   ↓
ClickHouse


⸻


ClickHouse Analytics
ClickHouse stores advertisement optimization events for analytics.
Database:
adstream
Table:
ad_events
The table stores:
user_id
page_id
recommended_position
ad_format
predicted_viewability
estimated_rpm
source
llm_used
latency_ms
event_time
The table uses:
MergeTree
with:
ORDER BY (event_time, page_id)


⸻


Security Implementation
The application includes multiple security measures.
Input Validation
Pydantic validates incoming API requests.
For example, scroll_depth must be between 0 and 100.
Invalid values return:
422 Unprocessable Content
Security Headers
The API includes headers such as:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
Content-Security-Policy: default-src 'self'
Secret Protection
Sensitive credentials are stored in:
.env
The .env file is excluded from Git using .gitignore.


⸻


Audit Logging
Audit logging is implemented using:
backend/app/audit_logger.py
Logs are stored in:
logs/audit.log
Example:
user_id=U101 | action=OPTIMIZE_PLACEMENT | status=SUCCESS | latency_ms=977.59
Cache hits are also recorded:
action=OPTIMIZE_PLACEMENT_CACHE_HIT | latency_ms=1.33


⸻


Docker Services
The project uses Docker Compose for infrastructure services.
Services:
redis-adstream
kafka-adstream
clickhouse-adstream
Start services using:
sudo docker compose up -d
[8/19/26 5:00 PM] Cherwin N: Check running services:
sudo docker ps
Stop services:
sudo docker compose down


⸻


Running the FastAPI Application
Activate the virtual environment:
source venv/bin/activate
Run FastAPI:
uvicorn backend.app.main:app --reload
Open Swagger UI:
http://127.0.0.1:8000/docs


⸻


Running the Kafka Consumer
Use:
python -m backend.app.consumer.kafka_consumer
The consumer receives Kafka events and stores them in ClickHouse.


⸻


Running Tests
Run:
python -m pytest -v
Final test result:
9 passed
0 failed
2 warnings
All core automated tests passed successfully.


⸻


Performance Results
Normal optimization request:
977.59 ms
Redis cached request:
1.33 ms
Redis significantly improved repeated request performance.


⸻


Test Coverage
The test suite verifies:
FastAPI root endpoint
Optimization endpoint
Invalid input validation
Redis cache key creation
Redis save
Redis retrieval
Kafka event publishing
ClickHouse timestamp conversion
ClickHouse event insertion


⸻


Documentation
Additional project documentation is available in:
docs/integration.md
docs/test-results.md
docs/security.md
docs/performance-results.md


⸻


Final Status
The project successfully implements:
FastAPI                    PASS
Redis Caching              PASS
Kafka Integration          PASS
Kafka Consumer             PASS
ClickHouse Storage         PASS
Input Validation           PASS
Audit Logging              PASS
Performance Optimization   PASS
Automated Testing          PASS
The AdStream Revenue Optimization backend is ready for final repository submission after completing the final GitHub cleanup.
=======
# AdStream Revenue Optimization Platform

## Project Overview

AdStream is an AI-powered Ad Tech revenue optimization platform that recommends suitable advertisement positions based on user behaviour.

The platform analyzes scroll depth, time spent on the page, device type, and page category. It predicts advertisement viewability, estimates RPM, generates a contextual explanation using Gemini, caches results in Redis, streams events through Kafka, and stores analytics data in ClickHouse.

## Project Objective

The objective is to improve advertisement viewability and publisher revenue by:

- Selecting suitable advertisement positions.
- Recommending display or native advertisement formats.
- Predicting advertisement viewability.
- Estimating Revenue Per Mille (RPM).
- Reducing response time through Redis caching.
- Processing advertisement events through Kafka.
- Storing events in ClickHouse for performance analysis.
- Validating the complete integration using automated tests.

## Technologies Used

| Technology | Purpose |
|---|---|
| FastAPI | Receives and processes optimization requests |
| Pydantic | Validates request data |
| Gemini LLM | Generates recommendation explanations |
| Redis | Caches optimization results |
| Apache Kafka | Streams advertisement events |
| ClickHouse | Stores and analyzes event data |
| Node.js | Provides the ad-placement management service |
| Docker | Runs Redis, Kafka, and ClickHouse |
| Pytest | Executes automated tests |
| Python | Implements optimization and integration logic |

## System Architecture

```text
Client
  │
  ▼
Node.js Ad Placement Service
  │
  ▼
FastAPI
  │
  ├──► Redis Cache
  │       ├── Cache hit → Return cached response
  │       └── Cache miss → Continue optimization
  │
  ├──► Ad Placement Optimizer
  │
  ├──► Gemini LLM
  │
  └──► Kafka Producer
           │
           ▼
       Kafka Topic
           │
           ▼
       Kafka Consumer
           │
           ▼
       ClickHouse
```

## Complete Data Flow

1. The client sends user behaviour data to the Node.js service.
2. Node.js forwards the request to FastAPI.
3. FastAPI validates the request using Pydantic.
4. FastAPI checks Redis for an existing result.
5. If a cached result exists, FastAPI returns it with `source: redis_cache`.
6. If no result exists, the optimization engine selects an advertisement position and format.
7. Gemini generates a short contextual explanation.
8. The completed result is stored in Redis.
9. FastAPI publishes the event to the Kafka `ad-events` topic.
10. The Kafka consumer receives the event.
11. The consumer inserts the event into ClickHouse.
12. ClickHouse stores the event for revenue and performance analysis.

## Features

- Scroll-based advertisement placement optimization.
- Dynamic advertisement format recommendation.
- Predicted advertisement viewability.
- Estimated RPM calculation.
- Gemini-generated recommendation explanation.
- Redis result caching.
- Kafka producer and consumer integration.
- ClickHouse analytics storage.
- Node.js to FastAPI communication.
- Pydantic input validation.
- Health-check endpoint.
- Swagger API documentation.
- Automated tests for normal and edge cases.
- Graceful handling of external service failures.

## Project Structure

```text
Task_3/
├── backend/
│   └── app/
│       ├── consumer/
│       │   ├── __init__.py
│       │   └── kafka_consumer.py
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── optimizer.py
│       ├── llm_service.py
│       ├── redis_service.py
│       └── kafka_producer.py
├── clickhouse/
│   └── init.sql
├── node-service/
│   ├── fastapiClient.js
│   ├── server.js
│   ├── package.json
│   └── package-lock.json
├── tests/
│   ├── test_api.py
│   ├── test_optimizer.py
│   ├── test_redis.py
│   ├── test_kafka.py
│   └── test_clickhouse.py
├── docs/
│   ├── integration.md
│   ├── test-results.md
│   └── screenshots/
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Environment Configuration

Create a `.env` file in the project folder:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.7-flash

REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_EXPIRY=300

KAFKA_SERVER=localhost:9092
KAFKA_TOPIC=ad-events

CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_USER=adstream
CLICKHOUSE_PASSWORD=adstream123
CLICKHOUSE_DATABASE=adstream

FASTAPI_URL=http://localhost:8000
```

The real `.env` file must not be uploaded to GitHub. Use `.env.example` to document the required variables.

## Installation

### 1. Create a Python virtual environment

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install Python packages

```bash
python -m pip install -r requirements.txt
```

### 3. Install Node.js packages

```bash
cd node-service
npm install
cd ..
```

## Running the Application

### 1. Start Docker services

```bash
docker compose up -d
```

The following containers should run:

```text
redis-adstream
kafka-adstream
clickhouse-adstream
```

Verify:

```bash
docker compose ps
```

### 2. Start FastAPI

```bash
python -m uvicorn backend.app.main:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

### 3. Start the Kafka consumer

Open another terminal:

```bash
python -m backend.app.consumer.kafka_consumer
```

Expected output:

```text
Connected to ClickHouse successfully
Connected to Kafka successfully
Kafka consumer started. Waiting for ad events...
```

### 4. Start Node.js

Open another terminal:

```bash
cd node-service
npm start
```

Node.js service:

```text
http://127.0.0.1:3000
```

## API Request Example

Endpoint:

```text
POST /optimize-placement
```

Request:

```json
{
  "user_id": "U105",
  "page_id": "P505",
  "scroll_depth": 72,
  "time_on_page": 50,
  "device_type": "mobile",
  "page_type": "technology"
}
```

Example response:

```json
{
  "user_id": "U105",
  "page_id": "P505",
  "recommended_position": "middle_content",
  "ad_format": "native",
  "predicted_viewability": 0.94,
  "estimated_rpm": 5.76,
  "reason": "A native advertisement in the middle content matches the user's active reading behaviour.",
  "source": "optimization_engine",
  "llm_used": true,
  "latency_ms": 120.5
}
```

## Redis Cache Validation

Send the same request twice.

The first request runs the optimizer and Gemini:

```json
{
  "source": "optimization_engine"
}
```

The second identical request returns the cached result:

```json
{
  "source": "redis_cache"
}
```

Redis can be verified using:

```bash
docker exec -it redis-adstream redis-cli ping
```

Expected result:

```text
PONG
```

## Kafka Validation

When FastAPI processes a request, the terminal should display:

```text
Kafka event published successfully: topic=ad-events
```

The consumer should display:

```text
Kafka event received
Event stored successfully in ClickHouse
```

## ClickHouse Validation

Run:

```bash
docker exec -it clickhouse-adstream clickhouse-client \
--user adstream \
--password adstream123 \
--query "SELECT * FROM adstream.ad_events"
```

The query should display stored advertisement events containing:

- User ID
- Page ID
- Advertisement position
- Advertisement format
- Predicted viewability
- Estimated RPM
- Response source
- LLM usage
- Latency
- Timestamp

## Node.js Integration Test

Send a request through Node.js:

```bash
curl -X POST http://127.0.0.1:3000/ad-placement \
-H "Content-Type: application/json" \
-d '{
  "user_id": "U106",
  "page_id": "P506",
  "scroll_depth": 75,
  "time_on_page": 55,
  "device_type": "mobile",
  "page_type": "technology"
}'
```

Node.js forwards the request to FastAPI and returns the optimization response.

## Automated Testing

Run all tests:

```bash
pytest -v
```

The test suite covers:

| Test scenario | Expected result |
|---|---|
| Valid API request | HTTP 200 response |
| Invalid scroll depth | HTTP 422 validation error |
| Empty user ID | HTTP 422 validation error |
| Low scroll depth | Top-content advertisement |
| Medium scroll depth | Middle-content advertisement |
| High scroll depth | Bottom-content advertisement |
| Redis cache hit | Cached response returned |
| Redis unavailable | API continues without crashing |
| Kafka publishing | Event published successfully |
| Kafka unavailable | Error handled without API failure |
| ClickHouse insertion | Event insertion executed |
| Gemini unavailable | Optimizer explanation used as fallback |

Detailed results are available in:

```text
docs/test-results.md
```

## Error Handling

The platform handles integration failures gracefully:

- If Gemini fails, the optimizer's original explanation is returned.
- If Redis is unavailable, the optimizer still processes the request.
- If Kafka is unavailable, FastAPI returns the recommendation without crashing.
- If invalid data is submitted, Pydantic returns an HTTP 422 response.
- If ClickHouse insertion fails, the consumer records the error without stopping the API.

## Integration Results

The following integration flow was successfully validated:

```text
Node.js → FastAPI → Redis → Optimizer → Gemini
FastAPI → Kafka Producer → Kafka Consumer → ClickHouse
```

The project demonstrates successful communication between API, caching, AI, event-streaming, and analytical-storage components.

## Security

- API keys are stored only in `.env`.
- `.env` is excluded through `.gitignore`.
- `.env.example` contains placeholders only.
- Generated folders such as `node_modules`, `venv`, and `__pycache__` are not committed.

## Documentation

Additional information is available in:

```text
docs/integration.md
docs/test-results.md
```
>>>>>>> decf7793b6653691dfc71006ae2743f1ba906d30
