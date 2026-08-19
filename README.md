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