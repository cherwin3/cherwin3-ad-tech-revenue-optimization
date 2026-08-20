 # AdStream Revenue Optimization API  
# Load Testing and Performance Evaluation Report

## 1. Introduction

The AdStream Revenue Optimization Platform is an AI-powered Ad Tech application designed to recommend suitable advertisement positions and formats based on user engagement behaviour. The system processes information such as scroll depth, time spent on the page, device type, and page type.

The backend application is developed using FastAPI. Redis is used as a caching service to improve response time and reduce repeated processing. The optimization engine calculates advertisement placement recommendations, while the Gemini Large Language Model can generate contextual explanations for the recommendations.

Because the platform may receive requests from many publisher websites and users simultaneously, it is important to evaluate its performance under load. Load testing helps determine whether the application can process multiple concurrent requests without producing excessive response delays or failures.

This report explains the load-testing environment, test scenarios, configuration, observed results, identified bottlenecks, and recommendations for improving the scalability and reliability of the AdStream API.

---

## 2. Purpose of Load Testing

The primary purpose of this load test is to measure the performance, stability, and reliability of the AdStream API when multiple simulated users access it simultaneously.

The load test was conducted to achieve the following objectives:

1. Determine whether the API can process multiple concurrent requests.
2. Measure the response time of the health and optimization endpoints.
3. Calculate the number of requests processed per second.
4. Identify failed requests and API errors.
5. Observe the behaviour of FastAPI and Redis during increased traffic.
6. Identify performance bottlenecks in the optimization and LLM services.
7. Verify that the API remains available throughout the test.
8. Provide recommendations for improving production performance.
9. Generate performance evidence for operational readiness.
10. Understand the approximate traffic level that the current system can support.

---

## 3. Scope of Testing

The load test focuses on the backend API of the AdStream Revenue Optimization Platform. The test simulates virtual users who repeatedly send requests to the application.

The following components were included in the test:

- FastAPI backend application.
- Uvicorn application server.
- Health-check endpoint.
- Advertisement-placement optimization endpoint.
- Pydantic request validation.
- Rule-based optimization engine.
- Redis caching service.
- Gemini explanation service, when available.
- Local machine network and system resources.

The following components were not fully included in the current local test:

- Apache Kafka event streaming.
- ClickHouse analytical database.
- React publisher dashboard.
- Production cloud infrastructure.
- Real publisher website traffic.
- Distributed Redis configuration.
- OpenTelemetry and Grafana monitoring.
- Production load balancer.

These components are part of the proposed enterprise architecture and can be included in future performance-testing stages.

---

## 4. Testing Tool

Locust was used to perform the load test.

Locust is an open-source performance-testing tool developed using Python. It allows developers to define user behaviour in a Python file and simulate multiple users sending HTTP requests to an application.

The Locust dashboard provides real-time performance information, including:

- Current number of simulated users.
- Total number of requests.
- Number of requests per second.
- Average response time.
- Minimum response time.
- Maximum response time.
- Response-time percentiles.
- Number and percentage of failed requests.
- Performance charts.
- Failure information.

Locust was selected because it is easy to integrate with Python and FastAPI applications. The virtual-user behaviour can be defined in a locustfile.py file, making the test repeatable and maintainable.

---

## 5. Test Environment
[8/20/26 12:19 AM] Cherwin N: The load test was performed in a local development environment.

| Component | Technology or configuration |
|---|---|
| Application | AdStream Revenue Optimization API |
| Programming language | Python |
| Backend framework | FastAPI |
| Application server | Uvicorn |
| Data validation | Pydantic |
| Caching service | Redis |
| Redis execution environment | Docker container |
| LLM service | Google Gemini API |
| Load-testing tool | Locust |
| API address | http://127.0.0.1:8000 |
| API documentation | http://127.0.0.1:8000/docs |
| Locust dashboard | http://localhost:8089 |
| Testing environment | Local development machine |
| Source-code management | Git and GitHub |

### Test machine details

- Operating system: [ENTER OPERATING SYSTEM]
- Processor: [ENTER PROCESSOR IF KNOWN]
- Installed memory: [ENTER RAM IF KNOWN]
- Python version: [ENTER PYTHON VERSION]
- Redis version: [ENTER VERSION IF KNOWN]
- Locust version: [ENTER VERSION IF KNOWN]

The results in this report represent the performance of the application on the local test machine. Production performance may be different because of server capacity, network speed, worker configuration, database capacity, and cloud infrastructure.

---

## 6. Application Architecture Under Test

The API receives user-engagement data and processes it through several application components.

The simplified request flow is:

Virtual Locust User
        ↓
FastAPI Endpoint
        ↓
Pydantic Input Validation
        ↓
Redis Cache Check
        ↓
Advertisement Optimization Engine
        ↓
Gemini Explanation Service
        ↓
Redis Result Storage
        ↓
JSON API Response

When a request reaches the optimization endpoint, FastAPI receives the request and Pydantic validates its data. The application checks Redis to determine whether a previously generated result is available.

If a cached result is available, the system can return it without repeating all processing. If no cached result exists, the optimization engine calculates a new recommendation. Gemini may then generate an explanation before the final response is returned.

This architecture supports fast request processing, reusable cached results, and understandable AI-generated recommendations.

---

## 7. Endpoints Tested

### 7.1 Health-check endpoint

- HTTP method: GET
- Endpoint: /health
- Complete URL: http://127.0.0.1:8000/health
- Purpose: Verify the availability of FastAPI and the Redis connection.

Example response:

{
  "api": "healthy",
  "redis": "connected"
}

The health endpoint is expected to respond quickly because it performs a limited service-status check.

### 7.2 Advertisement optimization endpoint

- HTTP method: POST
- Endpoint: /optimize-placement
- Complete URL: http://127.0.0.1:8000/optimize-placement
- Purpose: Generate an optimized advertisement-placement recommendation.

The following sample data was used during the load test:

{
  "user_id": "load-test-user",
  "page_id": "article-101",
  "scroll_depth": 65,
  "time_on_page": 45,
  "device_type": "desktop",
  "page_type": "article"
}

The optimization endpoint returns information similar to the following:

{
  "recommended_position": "middle_content",
  "ad_format": "native",
  "predicted_viewability": 0.94,
  "estimated_rpm": 5.76,
  "reason": "The user has demonstrated high engagement with the page.",
  "source": "optimization_engine",
  "llm_used": false
}

This endpoint performs more work than the health endpoint because it may use input validation, Redis, optimization logic, and the Gemini service.

---

## 8. Locust Test Script

The following Locust script was used to simulate user behaviour:
[8/20/26 12:19 AM] Cherwin N: from locust import HttpUser, task, between


class AdStreamUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def check_health(self):
        self.client.get(
            "/health",
            name="GET /health"
        )

    @task(3)
    def optimize_placement(self):
        payload = {
            "user_id": "load-test-user",
            "page_id": "article-101",
            "scroll_depth": 65,
            "time_on_page": 45,
            "device_type": "desktop",
            "page_type": "article"
        }

        self.client.post(
            "/optimize-placement",
            json=payload,
            name="POST /optimize-placement"
        )

The optimization task has a weight of three, while the health-check task has a weight of one. Therefore, a virtual user is more likely to call the optimization endpoint than the health endpoint.

A waiting period of one to three seconds is included between tasks. This creates a more realistic request pattern and prevents each virtual user from sending requests without any delay.

---

## 9. Test Preparation

Before conducting the test, the following preparation steps were completed.

### 9.1 Starting Redis

The Redis Docker container was started using:

sudo docker start redis-adstream

The container status was checked using:

sudo docker ps

The Redis connection was verified using:

sudo docker exec -it redis-adstream redis-cli ping

The expected response was:

PONG

### 9.2 Starting the FastAPI application

The application was started using:

uvicorn main:app --reload

The application health was verified by opening:

http://127.0.0.1:8000/health

### 9.3 Starting Locust

Locust was started using:

locust -f load-tests/locustfile.py --host http://127.0.0.1:8000

The Locust dashboard was opened using:

http://localhost:8089

The number of virtual users and the ramp-up rate were entered into the dashboard before starting the test.

---

## 10. Test Configuration

The following configuration was used for the completed load test:

| Configuration | Value |
|---|---:|
| Number of concurrent users | [ENTER USERS] |
| User ramp-up rate | [ENTER RATE] users/second |
| Test duration | [ENTER DURATION] |
| Wait time between requests | 1–3 seconds |
| Target host | http://127.0.0.1:8000 |
| Primary endpoint | POST /optimize-placement |
| Secondary endpoint | GET /health |
| Testing environment | Local machine |

### Meaning of concurrent users

The number of concurrent users represents the number of virtual users created by Locust. These are not real people. Each virtual user automatically sends requests according to the behaviour defined in locustfile.py.

### Meaning of ramp-up rate

The ramp-up rate defines how quickly Locust starts virtual users.

For example, a value of five means that Locust starts approximately five additional virtual users every second until the configured total number of users is reached.

---

## 11. Test Scenarios

### Scenario 1: Health-check testing

This scenario verifies whether the application remains available during the load test. Virtual users repeatedly call the /health endpoint.

The expected result is:

- HTTP status code 200.
- API status reported as healthy.
- Redis connection reported as connected.
- Low response time.
- No failed requests.

### Scenario 2: Optimization-endpoint testing

This scenario evaluates the performance of the main application functionality. Virtual users submit engagement data to /optimize-placement.

The expected result is:

- HTTP status code 200.
- Valid advertisement-position recommendation.
- Valid advertisement-format recommendation.
- Viewability and RPM values returned.
- Explanation included in the response.
- No validation or server errors.

### Scenario 3: Concurrent mixed traffic

This scenario combines health-check and optimization requests. It represents a situation where users access the primary application while monitoring software also checks the system's availability.

The expected result is that both endpoints remain available without a significant number of failures.

---
[8/20/26 12:19 AM] Cherwin N: ## 12. Overall Test Results

Enter the values displayed in the Aggregated row of the Locust Statistics page.

| Performance metric | Actual result |
|---|---:|
| Concurrent users | [ENTER RESULT] |
| Total requests | [ENTER RESULT] |
| Total failed requests | [ENTER RESULT] |
| Failure percentage | [ENTER RESULT]% |
| Requests per second | [ENTER RESULT] requests/second |
| Failures per second | [ENTER RESULT] |
| Average response time | [ENTER RESULT] ms |
| Minimum response time | [ENTER RESULT] ms |
| Maximum response time | [ENTER RESULT] ms |
| Median response time | [ENTER RESULT] ms |
| 95th-percentile response time | [ENTER RESULT] ms |
| 99th-percentile response time | [ENTER RESULT] ms |
| Total test duration | [ENTER RESULT] |

---

## 13. Endpoint-Level Results

Enter the separate values shown for each endpoint in Locust.

| Endpoint | Requests | Failures | Average time | Minimum time | Maximum time | Requests/second |
|---|---:|---:|---:|---:|---:|---:|
| GET /health | [VALUE] | [VALUE] | [VALUE] ms | [VALUE] ms | [VALUE] ms | [VALUE] |
| POST /optimize-placement | [VALUE] | [VALUE] | [VALUE] ms | [VALUE] ms | [VALUE] ms | [VALUE] |
| Aggregated | [VALUE] | [VALUE] | [VALUE] ms | [VALUE] ms | [VALUE] ms | [VALUE] |

---

## 14. Result Analysis

The AdStream API was tested with [ENTER USERS] concurrent virtual users and a ramp-up rate of [ENTER RATE] users per second. The test was allowed to run for approximately [ENTER DURATION].

During the test, the application processed a total of [ENTER REQUESTS] requests. The overall throughput was [ENTER RPS] requests per second.

The average response time was [ENTER AVERAGE] milliseconds, while the maximum recorded response time was [ENTER MAXIMUM] milliseconds. The failure percentage was [ENTER FAILURE]%.

### If your failure percentage is 0%

Use this paragraph:

The application completed the test without any failed requests. A failure rate of 0% indicates that the API remained stable and available for the selected user count and test duration. Therefore, the application successfully supported the simulated workload in the current local environment.

### If your failure percentage is greater than 0%

Use this paragraph:

Some requests failed during the load test. The failures indicate that one or more application components experienced difficulty under the selected traffic level. The failure information must be examined to determine whether the problem was caused by request timeouts, Redis connectivity, Gemini service limitations, invalid responses, or insufficient machine resources.

---

## 15. Comparison of Endpoint Performance

The /health endpoint is expected to have a lower response time because it performs only a basic service-status check. It does not execute the complete advertisement optimization process.

The /optimize-placement endpoint is expected to take more time because it performs several operations:

1. Receives and validates engagement information.
2. Creates or retrieves a Redis cache key.
3. Checks Redis for an existing result.
4. Runs the advertisement optimization logic when required.
5. Calculates predicted viewability and estimated RPM.
6. Calls Gemini when an AI-generated explanation is required.
7. Stores the completed response in Redis.
8. Returns the final JSON response.

If the optimization endpoint shows a significantly higher response time, the Gemini API call and Redis operations should be examined first.

---

## 16. Response-Time Evaluation

Response time represents how long the server takes to process a request and return a response.

The following general classification was used:

| Response time | Evaluation |
|---|---|
| Below 200 ms | Excellent for a local API request |
| 200–500 ms | Acceptable |
| 500–1000 ms | Requires observation |
| Above 1000 ms | Slow and requires optimization |
| Several seconds | Critical for real-time advertisement delivery |

For Ad Tech applications, low response time is especially important because advertisements must be selected and displayed before users scroll past the placement.
[8/20/26 12:19 AM] Cherwin N: The recorded average response time of [ENTER VALUE] ms is considered [EXCELLENT / ACCEPTABLE / SLOW] for the current test environment.

---

## 17. Throughput Evaluation

Throughput represents the number of requests processed by the application every second.

During the load test, the application achieved approximately [ENTER VALUE] requests per second.

A higher throughput indicates that the system can process more traffic. However, throughput must be evaluated together with response time and failure percentage. A high request rate is not useful if the API produces many failures or takes too long to respond.

The current throughput represents the performance of the local development configuration. A production deployment with multiple workers and larger computing resources may support a higher request rate.

---

## 18. Failure Analysis

The number of failed requests recorded during the test was [ENTER VALUE], producing a failure percentage of [ENTER VALUE]%.

Possible reasons for failed requests include:

- FastAPI server becoming unavailable.
- Redis connection failure.
- Gemini API timeout.
- Gemini API quota or permission error.
- Invalid request payload.
- Application exception.
- Excessive response time.
- Limited system CPU or memory.
- Network connectivity problems.
- Locust starting users too quickly.
- A single Uvicorn worker becoming overloaded.

If failures are displayed in the Locust Failures tab, their error messages should be recorded and investigated.

### Failure details

| Failed endpoint | Error message | Number of failures | Corrective action |
|---|---|---:|---|
| [ENDPOINT OR NONE] | [ERROR OR NO FAILURES] | [VALUE] | [ACTION] |

If no failures occurred, enter:

No failures were recorded during the test.

---

## 19. Identified Performance Bottlenecks

### 19.1 Gemini API latency

The Gemini API is an external service. Its response time depends on network speed, model availability, rate limits, and API quota. Calling Gemini for every request can significantly increase the optimization endpoint's response time.

### 19.2 Single Uvicorn worker

The development command normally starts a limited application configuration. A single worker may become a bottleneck when many requests arrive simultaneously.

### 19.3 Redis connection overhead

Redis generally provides fast access, but repeated connection creation or an unavailable Redis service can delay requests. A connection pool should be used for production workloads.

### 19.4 Repeated processing

If cache keys are not designed correctly, similar requests may repeatedly execute the complete optimization and LLM process instead of using cached results.

### 19.5 Local-machine limitations

FastAPI, Redis, Locust, and other services may all run on the same computer during testing. They compete for CPU and memory, which can reduce the accuracy of the performance test.

### 19.6 Development reload mode

The --reload option is useful during development, but it is not recommended for production performance testing. It watches source files and adds development overhead.

### 19.7 Synchronous external operations

If an external API call blocks the request-processing thread, other requests may wait longer. Asynchronous processing can improve concurrency.

---

## 20. Performance Recommendations

### 20.1 Improve Redis caching

Repeated optimization results should be stored in Redis with an appropriate expiration time. Proper cache keys should be generated from relevant request data.

### 20.2 Reduce Gemini calls

Gemini should not be called again when a suitable explanation is already cached. The application should also use a rule-based fallback if Gemini is unavailable.

### 20.3 Add API timeouts

A timeout should be configured for external Gemini requests. This prevents one slow external request from blocking the API for an excessive amount of time.

### 20.4 Use multiple workers

In production, Uvicorn can run with multiple workers:

uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
[8/20/26 12:19 AM] Cherwin N: The correct number of workers depends on the available processor cores and workload.

### 20.5 Add retry and fallback logic

Temporary Redis or Gemini errors should be handled safely. Retry attempts must be limited to prevent additional load.

### 20.6 Use Kafka for event processing

Advertisement impressions, clicks, scroll events, and viewability events can be sent to Kafka. This prevents analytical processing from delaying the main API response.

### 20.7 Use ClickHouse for analytics

ClickHouse can store and analyze large volumes of advertising events efficiently without overloading the operational API.

### 20.8 Add production monitoring

OpenTelemetry can collect application traces and metrics. Grafana dashboards can display request count, latency, error rate, Redis availability, CPU usage, and memory usage.

### 20.9 Repeat testing at different traffic levels

Future testing should include:

- 10 concurrent users.
- 50 concurrent users.
- 100 concurrent users.
- 250 concurrent users.
- Extended-duration stability testing.
- Sudden traffic-spike testing.

### 20.10 Separate test infrastructure

For more accurate results, Locust should run on a different machine from the FastAPI application. This prevents the load generator from consuming the same resources as the application being tested.

---

## 21. Operational Readiness Assessment

The system can be considered operationally ready for the tested traffic level when:

- The health endpoint remains available.
- Redis remains connected.
- The API returns valid responses.
- The failure percentage is close to 0%.
- Response time remains within the acceptable limit.
- No unhandled application exceptions occur.
- External-service failures use a safe fallback.
- Logs provide sufficient troubleshooting information.

Based on the completed test, the system [PASSED / PARTIALLY PASSED / FAILED] the operational-readiness assessment for [ENTER USERS] concurrent users.

### Suggested result statement

If you received 0% failures, write:

> The AdStream API successfully handled the simulated workload with no failed requests. The system remained stable throughout the test and demonstrated acceptable performance for the tested local configuration.

If failures occurred, write:

> The AdStream API processed most requests successfully, but some failures and increased response times were observed. Additional optimization and error-handling improvements are required before supporting the tested traffic level in production.

---

## 22. Test Limitations

The completed load test has the following limitations:

- The test was conducted on a local development machine.
- The test duration was limited.
- Simulated users used similar request data.
- Internet speed may have affected Gemini response time.
- The full production architecture was not deployed.
- Kafka and ClickHouse were not included in the request path.
- The test did not represent traffic from multiple geographical regions.
- Locust and the application may have shared the same computer.
- The test did not include complete production security controls.
- The results do not guarantee unlimited production capacity.

Therefore, the recorded user count should be treated as evidence of performance under the specific test conditions rather than a permanent capacity limit.

---

## 23. Future Testing Plan

The following performance tests are recommended for future development:

### Baseline test

Test the API with one user to determine the normal response time without concurrency.

### Load test

Gradually increase the number of users and observe normal performance under expected traffic.

### Stress test

Continue increasing users until response time becomes unacceptable or failures begin.

### Spike test

Introduce a sudden increase in users to evaluate how the system handles unexpected traffic.

### Endurance test

Run the test for several hours to identify memory leaks, connection problems, and long-term performance degradation.

### Failure-recovery test
[8/20/26 12:19 AM] Cherwin N: Stop Redis or simulate Gemini unavailability during the test to confirm that the application handles service failures correctly.

---

## 24. Test Evidence

The following screenshots should be stored inside the project:

docs/images/locust-statistics.png
docs/images/locust-charts.png

### Locust Statistics screenshot

The statistics screenshot should display:

- Endpoint names.
- Request count.
- Failure count.
- Median response time.
- Average response time.
- Minimum response time.
- Maximum response time.
- Requests per second.

Add the screenshot here after uploading it to the folder:

![Locust Statistics](images/locust-statistics.png)

### Locust Charts screenshot

The chart screenshot should display the changes in:

- Total requests per second.
- Response time.
- Number of active users.
- Failure count.

Add the screenshot here:

![Locust Performance Charts](images/locust-charts.png)

---

## 25. Final Conclusion

The Locust load test was conducted to evaluate the performance, stability, and operational readiness of the AdStream Revenue Optimization API under concurrent traffic.

The test simulated [ENTER USERS] users and processed [ENTER REQUESTS] requests. The application achieved an average throughput of [ENTER RPS] requests per second, with an average response time of [ENTER AVERAGE] milliseconds. The recorded failure percentage was [ENTER FAILURE]%.

The results show that the system [SUCCESSFULLY HANDLED / PARTIALLY HANDLED / DID NOT HANDLE] the selected traffic level in the local testing environment.

FastAPI provided an efficient API layer, while Redis supported faster access to repeated results. The external Gemini service may contribute additional response latency, so caching, timeouts, and fallback explanations should be maintained.

The platform can be improved further by using multiple API workers, optimizing Redis connections, reducing unnecessary Gemini calls, introducing Kafka for asynchronous event processing, storing analytics in ClickHouse, and monitoring production performance through OpenTelemetry and Grafana.

Overall, this load test provides measurable evidence of the current system's performance and identifies the technical improvements required for a reliable and scalable production deployment.