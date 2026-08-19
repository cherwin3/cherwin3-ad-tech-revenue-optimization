 Integration Flow
1. Overview
The AdStream Revenue Optimization platform integrates FastAPI, Redis, Kafka, ClickHouse, and the optimization engine into a single backend workflow.
The purpose of the integration is to process user scroll behavior, recommend the best ad placement, cache repeated requests for faster responses, publish events through Kafka, and store analytics data in ClickHouse.


⸻


2. End-to-End Data Flow
User / Client
     ↓
FastAPI API
     ↓
Pydantic Input Validation
     ↓
Redis Cache Check
     ↓
 ┌───────────────┐
 │ Cache Found?  │
 └───────────────┘
     ↓       ↓
    Yes      No
     ↓       ↓
Redis Result   Optimization Engine
     ↓             ↓
     └──────→ Response Preparation
                     ↓
                 Redis Cache
                     ↓
                 Kafka Producer
                     ↓
                 Kafka Topic
                     ↓
                 Kafka Consumer
                     ↓
                 ClickHouse
                     ↓
                 Analytics Storage


⸻


3. FastAPI Layer
FastAPI acts as the main backend API layer.
The main endpoint used for advertisement placement optimization is:
POST /optimize-placement
The endpoint receives user behavior information such as:
user_id
page_id
scroll_depth
time_on_page
device_type
page_type
FastAPI validates the request before processing it.


⸻


4. Input Validation
Pydantic models are used to validate incoming request data.
For example:
scroll_depth must be between 0 and 100
Invalid data is rejected with:
422 Unprocessable Content
This prevents incorrect or unsupported input from entering the optimization engine.


⸻


5. Redis Integration
Redis is used as a caching layer.
When an optimization request is received, the application first generates a cache key using the request data.
The application then checks Redis.
If the result already exists, the application returns the cached response immediately.
Example:
source = redis_cache
If the result does not exist, the application runs the optimization engine.
After the result is generated, it is stored in Redis for future requests.


⸻


6. Redis Performance Improvement
The same request was tested twice.
First request:
source = optimization_engine
latency_ms = 977.59
Second request:
source = redis_cache
latency_ms = 1.33
This demonstrates that Redis significantly reduces repeated request latency.


⸻


7. Optimization Engine
If no cached result exists, the request is processed by the optimization engine.
The engine uses user engagement data such as:
scroll_depth
time_on_page
device_type
page_type
It generates:
recommended_position
ad_format
predicted_viewability
estimated_rpm
reason
Example result:
recommended_position = middle_content
ad_format = native
predicted_viewability = 0.94
estimated_rpm = 5.76


⸻


8. LLM Integration
The system also contains an LLM service for generating contextual explanations for advertisement placement recommendations.
If the LLM returns a valid explanation, it replaces the default optimization reason.
The response contains:
llm_used = true
If the LLM is unavailable, the system continues using the optimization engine result.
This provides graceful fallback behavior.


⸻


9. Kafka Producer
After the optimization response is generated, the application creates an advertisement event.
The event contains fields such as:
user_id
page_id
recommended_position
ad_format
predicted_viewability
estimated_rpm
source
llm_used
latency_ms
timestamp
The FastAPI backend publishes this event to Kafka.
Terminal verification:
Kafka producer connected to localhost:9092
Kafka event published successfully


⸻


10. Kafka Consumer
The Kafka consumer listens for advertisement events.
The consumer was started using:
python -m backend.app.consumer.kafka_consumer
The consumer successfully connected to Kafka.
Example output:
Connected to Kafka successfully
Kafka consumer started. Waiting for ad events...
When an event is received, the consumer processes the event and prepares it for ClickHouse insertion.


⸻


11. ClickHouse Integration
[8/19/26 4:57 PM] Cherwin N: ClickHouse is used as the analytics database.
The database is:
adstream
The analytics table is:
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
ENGINE = MergeTree
with:
ORDER BY (event_time, page_id)
This structure supports efficient analytics queries.


⸻


12. Kafka to ClickHouse Flow
The complete event pipeline is:
FastAPI
   ↓
Kafka Producer
   ↓
Kafka Topic
   ↓
Kafka Consumer
   ↓
ClickHouse
The consumer successfully stored events in ClickHouse.
Terminal result:
Event stored successfully in ClickHouse


⸻


13. ClickHouse Verification
The stored events were verified using:
USE adstream;

SELECT * FROM ad_events LIMIT 10;
The query successfully returned stored optimization records.
Two records were observed:
optimization_engine request
redis_cache request
This confirmed that the complete event pipeline was functioning correctly.


⸻


14. Audit Logging Integration
The system records important API activity using:
backend/app/audit_logger.py
Audit information is stored in:
logs/audit.log
Example:
user_id=U101
action=OPTIMIZE_PLACEMENT
status=SUCCESS
latency_ms=977.59
Cache hits are also recorded:
action=OPTIMIZE_PLACEMENT_CACHE_HIT
latency_ms=1.33
This allows user and system activity to be tracked for auditing purposes.


⸻


15. Health Monitoring
The application provides:
GET /health
The endpoint verifies:
FastAPI status
Redis connection
Successful response:
{
  "api": "healthy",
  "redis": "connected"
}


⸻


16. Docker Integration
The infrastructure services are managed using Docker Compose.
The services include:
redis-adstream
kafka-adstream
clickhouse-adstream
The ports used are:
Redis       6379
Kafka       9092
ClickHouse  8123 / 9000
This provides an isolated and reproducible environment for the backend infrastructure.


⸻


17. Complete System Flow
Client Request
      ↓
FastAPI
      ↓
Pydantic Validation
      ↓
Redis Cache Check
      ↓
      ├── Cache Hit → Return Cached Result
      │
      └── Cache Miss
             ↓
      Optimization Engine
             ↓
         LLM Service
             ↓
         Save to Redis
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
             ↓
        Analytics Data

At the same time:

FastAPI
   ↓
Audit Logger
   ↓
logs/audit.log


⸻


18. Integration Test Result
The following integrations were successfully verified:
FastAPI → Redis               PASS
FastAPI → Optimization Engine PASS
FastAPI → Kafka               PASS
Kafka → Consumer              PASS
Consumer → ClickHouse         PASS
FastAPI → Audit Logging       PASS
Redis Cache Hit               PASS
Input Validation              PASS


⸻


19. Conclusion
The AdStream Revenue Optimization platform successfully integrates API processing, caching, event streaming, analytics storage, and audit logging.
Redis improves API performance for repeated requests, Kafka provides asynchronous event streaming, ClickHouse stores optimization events for analytics, and audit logging records important system activity.
The complete integration flow was tested successfully.