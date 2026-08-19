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