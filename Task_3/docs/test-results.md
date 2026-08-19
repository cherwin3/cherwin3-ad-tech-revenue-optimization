# Automated Test Results

## 1. Test Objective

The purpose of testing is to verify that the AdStream platform correctly handles normal requests, invalid input, caching, event publishing, ClickHouse insertion, and external service failures.

## 2. Test Environment

| Item | Value |
|---|---|
| Operating system | Ubuntu Linux / Windows |
| Python test framework | Pytest |
| API framework | FastAPI |
| Cache | Redis |
| Event broker | Apache Kafka |
| Analytics database | ClickHouse |
| AI service | Gemini |
| Container platform | Docker |

## 3. Command Used

```bash
pytest -v
```

## 4. Test Cases

| ID | Test case | Expected result | Actual result | Status |
|---|---|---|---|---|
| TC-01 | API root endpoint | Returns HTTP 200 | HTTP 200 returned | Pass |
| TC-02 | Valid optimization request | Returns recommendation | Recommendation returned | Pass |
| TC-03 | Invalid scroll depth above 100 | Returns HTTP 422 | HTTP 422 returned | Pass |
| TC-04 | Empty user ID | Returns HTTP 422 | HTTP 422 returned | Pass |
| TC-05 | Low scroll depth | Selects `top_content` | `top_content` selected | Pass |
| TC-06 | Medium scroll depth | Selects `middle_content` | `middle_content` selected | Pass |
| TC-07 | High scroll depth | Selects `bottom_content` | `bottom_content` selected | Pass |
| TC-08 | High engagement time | Increases viewability | Viewability increased | Pass |
| TC-09 | Redis cache key | Creates stable cache key | Cache key created | Pass |
| TC-10 | Redis cache write | Calls Redis `setex` | Cache write verified | Pass |
| TC-11 | Redis cache read | Returns stored result | Cached result returned | Pass |
| TC-12 | Redis unavailable | API continues safely | Failure handled | Pass |
| TC-13 | Kafka publishing | Sends event to `ad-events` | Event publishing verified | Pass |
| TC-14 | Kafka unavailable | Returns `False` without crash | Failure handled | Pass |
| TC-15 | Timestamp conversion | Converts ISO timestamp | Timestamp converted | Pass |
| TC-16 | ClickHouse insertion | Calls database insertion | Insertion verified | Pass |
| TC-17 | Gemini unavailable | Uses optimizer reason | Fallback reason returned | Pass |
| TC-18 | Node.js integration | Forwards request to FastAPI | Response received | Pass |

## 5. API Validation Results

### Valid request

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

Result:

```text
HTTP 200 OK
```

The response contained:

- Recommended position
- Advertisement format
- Predicted viewability
- Estimated RPM
- Recommendation reason
- Response source
- LLM usage
- Latency

### Invalid request

A scroll depth greater than 100 was submitted.

Expected and actual result:

```text
HTTP 422 Unprocessable Entity
```

## 6. Redis Test Results

Redis connection:

```bash
docker exec -it redis-adstream redis-cli ping
```

Result:

```text
PONG
```

First request:

```json
{
  "source": "optimization_engine"
}
```

Second identical request:

```json
{
  "source": "redis_cache"
}
```

Result: Redis caching works correctly.

## 7. Gemini Test Result

When Gemini successfully generated the explanation:

```json
{
  "llm_used": true
}
```

When Gemini was unavailable, the API returned the optimizer's original reason without crashing.

Result: Gemini integration and fallback behaviour work correctly.

## 8. Kafka Test Result

Producer output:

```text
Kafka event published successfully:
topic=ad-events, partition=0, offset=0
```

Consumer output:

```text
Kafka event received
Event stored successfully in ClickHouse
```

Result: Kafka producer and consumer communication works correctly.

## 9. ClickHouse Test Result

Verification query:

```sql
SELECT * FROM adstream.ad_events;
```

A row containing the processed advertisement event was returned.

Result: Kafka events are successfully inserted into ClickHouse.

## 10. Node.js Integration Result

Node.js endpoint:

```text
POST http://127.0.0.1:3000/ad-placement
```

The service forwarded the request to FastAPI and returned:

```json
{
  "status": "success"
}
```

Result: Node.js to FastAPI integration works correctly.

## 11. Edge Cases Covered

The test suite covers:

- Scroll depth below the normal range.
- Scroll depth above the valid range.
- Empty identifiers.
- Low user engagement.
- High user engagement.
- Redis cache hit and cache miss.
- Redis connection failure.
- Kafka publishing failure.
- Gemini failure.
- Empty Gemini response.
- ClickHouse insertion.
- Invalid request data.

## 12. Test Summary

| Category | Result |
|---|---|
| API testing | Passed |
| Input validation | Passed |
| Optimizer testing | Passed |
| Redis testing | Passed |
| Gemini fallback testing | Passed |
| Kafka testing | Passed |
| ClickHouse testing | Passed |
| Node.js integration | Passed |
| Overall result | Passed |

## 13. Conclusion

The tests verify that the platform handles typical operations and important edge cases. External service failures are handled without crashing the FastAPI application. The complete integration between Node.js, FastAPI, Redis, Gemini, Kafka, and ClickHouse was validated successfully.

## 14. Evidence

Screenshots should be stored in:

```text
docs/screenshots/
```

Recommended screenshots:

```text
fastapi-response.png
invalid-request.png
llm-true.png
redis-cache.png
kafka-producer.png
kafka-consumer.png
clickhouse-row.png
node-fastapi.png
pytest-results.png
```