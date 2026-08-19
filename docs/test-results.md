Test Results
1. Test Objective
The purpose of testing was to verify that the AdStream Revenue Optimization API works correctly across its main components, including FastAPI, Redis caching, Kafka messaging, ClickHouse storage, input validation, and audit logging.
The tests were executed using pytest inside the Python virtual environment.


⸻


2. Test Command
python -m pytest -v


⸻


3. Final Automated Test Result
The final automated test execution produced the following result:
Total Tests Collected: 9
Passed Tests: 9
Failed Tests: 0
Warnings: 2
Overall Status: PASS
Final pytest summary:
9 passed, 2 warnings in 2.66s
The warnings did not cause any test failures.


⸻


4. Automated Test Cases
Test 1: Root API Endpoint
Test file:
tests/test_api.py
Test name:
test_root
Purpose:
This test verifies that the main FastAPI root endpoint is available and returns a successful response.
Result:
PASSED
Status: PASS


⸻


Test 2: Optimize Placement Endpoint
Test file:
tests/test_api.py
Test name:
test_optimize_placement
Purpose:
This test verifies that the /optimize-placement endpoint accepts valid input and returns an advertisement placement recommendation.
The endpoint processes user scroll behavior and returns information such as:
Recommended ad position
Ad format
Predicted viewability
Estimated RPM
Response source
Latency
Result:
PASSED
Status: PASS


⸻


Test 3: Invalid Scroll Depth Validation
Test file:
tests/test_api.py
Test name:
test_invalid_scroll_depth
Purpose:
This test verifies that invalid scroll depth values are rejected by Pydantic validation.
Example invalid value:
scroll_depth = 150
The valid range is between:
0 and 100
Expected result:
422 Unprocessable Content
Actual result:
422 Unprocessable Content
Status: PASS


⸻


Test 4: ClickHouse Timestamp Conversion
Test file:
tests/test_clickhouse.py
Test name:
test_convert_timestamp
Purpose:
This test verifies that the event timestamp can be converted into the correct format before being inserted into ClickHouse.
Result:
PASSED
Status: PASS


⸻


Test 5: ClickHouse Event Insertion
Test file:
tests/test_clickhouse.py
Test name:
test_insert_event
Purpose:
This test verifies that optimization event data can be inserted successfully into the ClickHouse analytics database.
Result:
PASSED
Status: PASS


⸻


Test 6: Kafka Event Publishing
Test file:
tests/test_kafka.py
Test name:
test_publish_ad_event
Purpose:
This test verifies that optimization events can be successfully published to the Kafka topic.
The system uses Kafka to transfer events asynchronously from the FastAPI application to downstream analytics processing.
Result:
PASSED
Status: PASS


⸻


Test 7: Redis Cache Key Creation
Test file:
tests/test_redis.py
Test name:
test_create_cache_key
Purpose:
This test verifies that the application generates a valid and consistent cache key from API request data.
Consistent cache keys are important because identical requests must retrieve the same cached response.
Result:
PASSED
Status: PASS


⸻


Test 8: Redis Cache Save
Test file:
tests/test_redis.py
Test name:
test_save_cached_result
Purpose:
This test verifies that optimization results can be successfully saved in Redis.
Result:
PASSED
Status: PASS


⸻


Test 9: Redis Cache Retrieval
Test file:
tests/test_redis.py
Test name:
test_get_cached_result
Purpose:
This test verifies that previously cached optimization results can be successfully retrieved from Redis.
Result:
PASSED
Status: PASS


⸻


5. Redis Connectivity Test
Redis was tested directly using:
sudo docker exec -it redis-adstream redis-cli ping
Expected response:
PONG
Actual response:
PONG
Status: PASS


⸻


6. FastAPI Health Check Test
The FastAPI health endpoint was tested using:
GET /health
Successful response:
{
  "api": "healthy",
  "redis": "connected"
}
HTTP status:
200 OK
Status: PASS


⸻


7. Redis Cache Performance Test
The Redis cache was tested by sending the same /optimize-placement request twice.
First Request
The first request was processed by the complete optimization engine.
Result:
source = optimization_engine
latency_ms = 977.59
Second Request
[8/19/26 4:54 PM] Cherwin N: The identical request was returned from Redis cache.
Result:
source = redis_cache
latency_ms = 1.33
Performance Comparison
Normal optimization request:
977.59 ms
Redis cached request:
1.33 ms
The cached request was significantly faster than the original optimization request.
Status: PASS


⸻


8. Kafka Producer Test
The FastAPI application successfully connected to Kafka.
Terminal output confirmed:
Kafka producer connected to localhost:9092
The event was successfully published:
Kafka event published successfully
Status: PASS


⸻


9. Kafka Consumer Test
The Kafka consumer was started using the backend consumer module.
The consumer successfully connected to Kafka and waited for advertisement events.
Terminal output confirmed:
Connected to Kafka successfully
Kafka consumer started. Waiting for ad events...
The consumer successfully received optimization events.
Status: PASS


⸻


10. ClickHouse Connectivity Test
The Kafka consumer successfully connected to ClickHouse.
Terminal result:
Connected to ClickHouse successfully
Status: PASS


⸻


11. Kafka to ClickHouse Integration Test
The complete event processing flow was tested:
FastAPI
   ↓
Kafka Producer
   ↓
Kafka Topic
   ↓
Kafka Consumer
   ↓
ClickHouse
The consumer received events and stored them successfully.
Terminal result:
Event stored successfully in ClickHouse
Status: PASS


⸻


12. ClickHouse Data Verification
The ClickHouse database used was:
adstream
The table used was:
ad_events
The following query was executed:
SELECT * FROM ad_events LIMIT 10;
Two event records were successfully displayed.
The records included data such as:
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
The table contained both:
source = optimization_engine
and:
source = redis_cache
Status: PASS


⸻


13. Audit Logging Test
Audit logging was implemented using:
backend/app/audit_logger.py
Audit data was stored in:
logs/audit.log
The log successfully recorded optimization activity.
Example normal request:
user_id=U101 | action=OPTIMIZE_PLACEMENT | status=SUCCESS | latency_ms=977.59
Example Redis cache request:
user_id=U101 | action=OPTIMIZE_PLACEMENT_CACHE_HIT | status=SUCCESS | latency_ms=1.33
This confirms that user actions, status, and latency are successfully recorded.
Status: PASS


⸻


14. Input Validation Test
An invalid request was tested using:
{
  "user_id": "U101",
  "page_id": "P501",
  "scroll_depth": 150,
  "time_on_page": 45,
  "device_type": "mobile",
  "page_type": "news"
}
Because scroll_depth exceeds the allowed maximum value of 100, FastAPI rejected the request.
Result:
422 Unprocessable Content
Status: PASS


⸻


15. Page Type Validation Test
An unsupported page type such as:
article
was tested.
The application only accepts configured values such as:
news
sports
technology
entertainment
finance
other
The invalid page type was rejected with:
422 Unprocessable Content
Status: PASS


⸻


16. Security Headers Test
The application includes HTTP security headers such as:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
Content-Security-Policy: default-src 'self'
These headers help reduce common browser-based security risks.
Status: PASS


⸻


17. API Key Protection Test
Sensitive credentials are stored in:
.env
The .env file is protected using:
.gitignore
This prevents API keys from being accidentally uploaded to GitHub.
Status: PASS


⸻


18. Docker Service Test
The required backend infrastructure was started using Docker.
The running services included:
redis-adstream
kafka-adstream
clickhouse-adstream
Docker port mappings were verified.
Redis:
6379:6379
Kafka:
9092:9092
ClickHouse:
8123:8123
9000:9000
Status: PASS


⸻


19. Test Summary
Test Area
Status
FastAPI Root Endpoint
PASS
Optimize Placement Endpoint
PASS
Input Validation
PASS
Invalid Scroll Depth
PASS
Page Type Validation
PASS
Redis Connection
PASS
Redis Cache Save
PASS
Redis Cache Retrieval
PASS
Redis Cache Performance
PASS
Kafka Producer
PASS
Kafka Consumer
PASS
ClickHouse Connection
PASS
[8/19/26 4:54 PM] Cherwin N: ClickHouse Event Insert
PASS
Kafka → ClickHouse Integration
PASS
Audit Logging
PASS
Security Headers
PASS
Secret Protection
PASS
Docker Services
PASS
Automated Pytest Suite
PASS


⸻


20. Overall Test Result
The final automated test suite produced:
9 passed
0 failed
2 warnings
The two warnings were dependency deprecation warnings and did not affect the execution or correctness of the application.
The major platform components were successfully tested:
FastAPI          PASS
Redis            PASS
Kafka            PASS
ClickHouse       PASS
Audit Logging    PASS
Input Validation PASS
Performance      PASS
Security         PASS
Final Status
ALL CORE TESTS PASSED SUCCESSFULLY
The AdStream Revenue Optimization backend is functioning correctly across API processing, caching, event streaming, analytics storage, validation, security controls, and audit logging.