# AdStream Revenue Optimization Platform

# Maintenance Guide

## 1. Introduction

The AdStream Revenue Optimization Platform is an AI-powered Ad Tech system that analyzes user engagement and recommends an appropriate advertisement position and format.

The platform uses FastAPI for the backend API, Redis for caching, Docker for running Redis, Gemini for generating contextual explanations, and Locust for performance testing.

Regular maintenance is required to ensure that the platform continues to operate reliably, securely, and efficiently. Maintenance activities help identify service failures, reduce downtime, improve response time, protect API credentials, and ensure that all software dependencies remain updated.

This document provides detailed daily, weekly, and monthly maintenance procedures for the AdStream Revenue Optimization Platform.

---

## 2. Purpose of the Maintenance Guide

The purpose of this guide is to provide clear procedures for maintaining all important components of the platform.

This guide helps the operational team to:

- Keep FastAPI and Redis services available.
- Identify system errors at an early stage.
- Maintain acceptable API response times.
- Prevent unnecessary service downtime.
- Review and manage Redis cached data.
- Protect Gemini API credentials.
- Update Python dependencies safely.
- Perform regular load testing.
- Test recovery procedures.
- Maintain accurate project documentation.
- Back up the source code using GitHub.
- Improve the long-term reliability of the system.

---

## 3. System Components

The following components require regular maintenance:

| Component | Purpose |
|---|---|
| FastAPI | Provides the backend REST API |
| Uvicorn | Runs the FastAPI application |
| Pydantic | Validates incoming request data |
| Redis | Caches optimization responses |
| Docker | Runs Redis in an isolated container |
| Gemini API | Generates contextual explanations |
| Optimization engine | Recommends advertisement positions |
| Locust | Performs API load testing |
| Git | Tracks source-code changes |
| GitHub | Stores source code and documentation |

---

## 4. Maintenance Objectives

The main objectives of platform maintenance are:

1. Ensure that the API remains available.
2. Confirm that Redis is running and connected.
3. Detect and resolve FastAPI errors.
4. Monitor API response times.
5. Prevent Redis memory problems.
6. Verify that Gemini works correctly.
7. Maintain the rule-based explanation fallback.
8. Protect sensitive API credentials.
9. Keep software dependencies updated.
10. Test the system under simulated traffic.
11. Maintain current technical documentation.
12. Verify backup and recovery procedures.

---

## 5. Daily Maintenance Procedures

Daily maintenance should be performed whenever the application is actively used.

### 5.1 Check the FastAPI health endpoint

Open the following URL:

```text
http://127.0.0.1:8000/health
```

The expected response is:

```json
{
  "api": "healthy",
  "redis": "connected"
}
```

The same check can be performed through the terminal:

```bash
curl http://127.0.0.1:8000/health
```

If the health endpoint does not open, check whether FastAPI is running.

---

### 5.2 Check the Redis container

Run:

```bash
sudo docker ps
```

Confirm that the container named `redis-adstream` is displayed and its status is `Up`.

If the container is stopped, start it:

```bash
sudo docker start redis-adstream
```

---

### 5.3 Verify the Redis connection

Run:

```bash
sudo docker exec -it redis-adstream redis-cli ping
```

Expected result:

```text
PONG
```

A `PONG` response confirms that the Redis server is operating correctly.

If Redis does not return `PONG`, restart it:

```bash
sudo docker restart redis-adstream
```

---

### 5.4 Test the optimization endpoint

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Select:

```text
POST /optimize-placement
```

Use the following request:

```json
{
  "user_id": "maintenance-user",
  "page_id": "article-101",
  "scroll_depth": 65,
  "time_on_page": 45,
  "device_type": "desktop",
  "page_type": "article"
}
```

The response should contain:

- Recommended advertisement position.
- Advertisement format.
- Predicted viewability.
- Estimated RPM.
- Explanation.
- Recommendation source.
- LLM usage status.

The HTTP response status should be:

```text
200 OK
```

---

### 5.5 Review FastAPI logs

The Uvicorn terminal should be checked for:

- Python exceptions.
- Redis connection failures.
- Gemini API errors.
- Request validation failures.
- HTTP 500 errors.
- Slow API responses.
- Application startup failures.

Successful requests normally appear as:

```text
200 OK
```

If repeated errors are found, record the error message and investigate the affected component.

---

### 5.6 Daily checklist

- [ ] FastAPI is running.
- [ ] `/health` returns a healthy response.
- [ ] Redis container status is `Up`.
- [ ] Redis returns `PONG`.
- [ ] `/optimize-placement` returns status code `200`.
- [ ] No critical errors appear in FastAPI logs.
- [ ] Gemini works or the fallback explanation is available.
- [ ] API response time is acceptable.

---

## 6. Weekly Maintenance Procedures

Weekly maintenance helps identify problems that may not be visible during daily checks.

### 6.1 Review Redis logs

Run:

```bash
sudo docker logs redis-adstream
```

To continuously monitor logs:

```bash
sudo docker logs -f redis-adstream
```

Press `Ctrl + C` to stop viewing continuous logs.

Look for:

- Unexpected container restarts.
- Memory warnings.
- Connection failures.
- Persistence errors.
- Redis startup errors.

---

### 6.2 Check Redis memory usage

Run:

```bash
sudo docker exec -it redis-adstream redis-cli info memory
```

Review the following information:

- Used memory.
- Maximum memory.
- Memory fragmentation.
- Number of cached keys.
- Memory allocation.

High Redis memory usage can reduce performance or cause the service to reject new data.

---

### 6.3 Check the number of cached keys

Run:

```bash
sudo docker exec -it redis-adstream redis-cli dbsize
```

This command shows the number of keys stored in the current Redis database.

A continuously increasing key count may indicate that cached results do not have an expiration time.

Redis cache entries should use an appropriate Time to Live value so that outdated results are removed automatically.

---

### 6.4 Review Gemini service errors

Review the FastAPI terminal for errors such as:

- Invalid API key.
- Permission denied.
- Model not found.
- Request timeout.
- Rate limit exceeded.
- Quota exceeded.
- Network connection failure.

If Gemini fails, the platform should continue using the rule-based explanation.

The response should contain:

```json
{
  "llm_used": false
}
```

This is an expected fallback response and does not mean that the complete optimization API has failed.

---

### 6.5 Check disk space

Run:

```bash
df -h
```

Check whether the disk has sufficient available space.

Insufficient disk space can affect:

- Docker containers.
- Application logs.
- Python packages.
- Git operations.
- Redis persistence.
- Test-result storage.

---

### 6.6 Verify Git security

Run:

```bash
git status
```

Confirm that `.env` is not listed as a file waiting to be committed.

The `.gitignore` file should contain:

```text
.env
venv/
__pycache__/
*.pyc
```

The Gemini API key must never be uploaded to GitHub.

---

### 6.7 Weekly checklist

- [ ] Redis logs were reviewed.
- [ ] Redis memory usage was checked.
- [ ] Cached-key count was checked.
- [ ] Gemini errors were reviewed.
- [ ] Disk space was checked.
- [ ] `.env` remains protected.
- [ ] Rule-based fallback was tested.
- [ ] Application documentation is current.

---

## 7. Monthly Maintenance Procedures

Monthly maintenance focuses on performance, security, dependencies, documentation, and recovery testing.

### 7.1 Review Python dependencies

Display installed packages:

```bash
pip list
```

Display outdated packages:

```bash
pip list --outdated
```

Update a package only after checking its compatibility:

```bash
pip install --upgrade package-name
```

After testing, update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Do not update every package without testing the application.

---

### 7.2 Verify the application after updates

After updating dependencies:

1. Start Redis.
2. Start FastAPI.
3. Open `/health`.
4. Test `/optimize-placement`.
5. Check the Gemini integration.
6. Test the fallback explanation.
7. Run a small Locust test.
8. Review all application logs.

If an update causes a failure, restore the previous compatible package version.

---

### 7.3 Perform load testing

Start Locust:

```bash
locust -f load-tests/locustfile.py --host http://127.0.0.1:8000
```

Open the dashboard:

```text
http://localhost:8089
```

Recommended test levels:

| Test | Users | Ramp-up rate | Duration |
|---|---:|---:|---:|
| Basic test | 10 | 2 users/second | 1 minute |
| Normal test | 50 | 5 users/second | 2 minutes |
| High-load test | 100 | 10 users/second | 2 minutes |

Record:

- Total requests.
- Requests per second.
- Average response time.
- Minimum response time.
- Maximum response time.
- Failure percentage.
- Error messages.

Update:

```text
docs/load-test-report.md
```

---

### 7.4 Review performance trends

Compare the current Locust results with previous results.

Investigate if:

- Average response time increased.
- Maximum response time increased.
- Requests per second decreased.
- Failure percentage increased.
- Redis memory usage increased.
- Gemini calls became slower.
- CPU or memory usage increased.

Performance deterioration may indicate a code problem, cache problem, dependency issue, external API delay, or insufficient computing resources.

---

### 7.5 Review security configuration

Check the following:

- `.env` is ignored by Git.
- Gemini API key is active.
- Exposed API keys have been rotated.
- Logs do not contain secret information.
- Redis is not publicly accessible.
- Request validation is enabled.
- Dependencies do not contain known vulnerabilities.
- HTTPS is planned for production.
- Authentication is planned before public deployment.

---

### 7.6 Review documentation

Review and update:

```text
README.md
docs/architecture.md
docs/design-decisions.md
docs/operational-runbook.md
docs/maintenance-guide.md
docs/load-test-report.md
```

Documentation must reflect the current code, endpoints, technologies, and operating procedures.

---

### 7.7 Monthly checklist

- [ ] Dependencies were reviewed.
- [ ] The application was tested after updates.
- [ ] Locust load testing was completed.
- [ ] Performance results were compared.
- [ ] Security settings were reviewed.
- [ ] Recovery procedures were tested.
- [ ] Documentation was updated.
- [ ] GitHub backup was verified.

---

## 8. FastAPI Maintenance

### 8.1 Start FastAPI

Move to the project folder:

```bash
cd ~/Downloads/Telegram\ Desktop/Cherwin_project
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

---

### 8.2 Restart FastAPI

Stop the application using:

```text
Ctrl + C
```

Start it again:

```bash
uvicorn main:app --reload
```

Verify:

```text
http://127.0.0.1:8000/health
```

---

### 8.3 Production execution

For a production-like environment:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Multiple workers can improve concurrent request processing.

The `--reload` option should not be used in production.

---

### 8.4 FastAPI error codes

| Status code | Meaning | Maintenance action |
|---|---|---|
| `200` | Successful request | No action required |
| `404` | Endpoint not found | Verify the URL |
| `422` | Invalid request data | Verify JSON fields |
| `500` | Internal server error | Check FastAPI logs |
| `502` | External service error | Check Gemini or Redis |
| `503` | Service unavailable | Check service status |

---

## 9. Redis Maintenance

### 9.1 Start Redis

```bash
sudo docker start redis-adstream
```

### 9.2 Stop Redis

```bash
sudo docker stop redis-adstream
```

### 9.3 Restart Redis

```bash
sudo docker restart redis-adstream
```

### 9.4 Check Redis status

```bash
sudo docker ps
```

### 9.5 Test Redis

```bash
sudo docker exec -it redis-adstream redis-cli ping
```

Expected result:

```text
PONG
```

### 9.6 Check Redis information

```bash
sudo docker exec -it redis-adstream redis-cli info
```

### 9.7 Check cached-key count

```bash
sudo docker exec -it redis-adstream redis-cli dbsize
```

### 9.8 Clear the cache

```bash
sudo docker exec -it redis-adstream redis-cli FLUSHDB
```

Expected response:

```text
OK
```

`FLUSHDB` removes all cached keys from the selected database. It should not be used during normal production operation without authorization.

---

## 10. Gemini Integration Maintenance

Gemini generates contextual explanations for the optimization result.

The following problems may affect Gemini:

- Missing API key.
- Invalid API key.
- Permission denied.
- Unsupported model.
- Rate limit exceeded.
- Quota exhausted.
- Network connection failure.
- Request timeout.

The API key must be stored in:

```text
.env
```

Example:

```env
GEMINI_API_KEY=your_actual_api_key
```

Never include the actual key in:

- Python files.
- README files.
- Screenshots.
- GitHub commits.
- Load-test reports.
- Presentations.

If Gemini becomes unavailable, the system should use a rule-based explanation and return:

```json
{
  "llm_used": false
}
```

This fallback ensures that the optimization service remains available.

---

## 11. Cache Maintenance Strategy

Redis stores frequently requested optimization results.

Caching provides the following benefits:

- Reduces repeated calculations.
- Reduces repeated Gemini calls.
- Improves response time.
- Reduces external API usage.
- Supports a higher number of users.

Cache entries should have an expiration time. Old or invalid results should not remain permanently.

Cache keys should be created using relevant input values, such as:

- Page ID.
- Scroll-depth range.
- Time-on-page range.
- Device type.
- Page type.

The cache should be cleared only when:

- Cache logic changes.
- Cached responses are invalid.
- Testing requires an empty database.
- An authorized maintenance procedure requires it.

---

## 12. Log Management

Logs help the operational team understand what happened before and during a failure.

The logs should record:

- Request endpoint.
- HTTP response code.
- Error type.
- Service status.
- Redis connection failures.
- Gemini failures.
- Response time.
- Application startup and shutdown.

Logs must not record:

- Gemini API keys.
- Passwords.
- Personal information.
- Secret environment variables.
- Authentication tokens.

Redis logs can be checked using:

```bash
sudo docker logs redis-adstream
```

Docker resource usage can be monitored using:

```bash
sudo docker stats redis-adstream
```

---

## 13. Performance Monitoring

Important performance metrics include:

| Metric | Purpose |
|---|---|
| Request count | Shows application usage |
| Requests per second | Measures throughput |
| Average response time | Shows normal API speed |
| Maximum response time | Identifies slow requests |
| Failure percentage | Shows service reliability |
| CPU usage | Shows processing demand |
| Memory usage | Detects resource problems |
| Redis memory | Monitors cache consumption |
| Gemini latency | Measures external-service delay |

OpenTelemetry and Grafana can be added in a production environment to collect and display these metrics continuously.

---

## 14. Backup Procedures

The source code and documentation should be backed up in GitHub.

Before important maintenance:

```bash
git status
git add .
git commit -m "Create maintenance checkpoint"
git push origin main
```

The following items should be included:

- Application source code.
- `requirements.txt`.
- Architecture documentation.
- Operational runbook.
- Maintenance guide.
- Load-test report.
- Locust test file.
- Test screenshots.
- Knowledge-transfer presentation.

The following items must not be uploaded:

- `.env`.
- API keys.
- Virtual environment.
- Python cache files.
- Local secret files.

---

## 15. Recovery Procedures

### 15.1 Redis recovery

If Redis fails:

1. Check its status:

```bash
sudo docker ps -a
```

2. Review logs:

```bash
sudo docker logs redis-adstream
```

3. Restart Redis:

```bash
sudo docker restart redis-adstream
```

4. Test Redis:

```bash
sudo docker exec -it redis-adstream redis-cli ping
```

5. Verify `/health`.

---

### 15.2 FastAPI recovery

If FastAPI fails:

1. Review the Uvicorn terminal.
2. Record the Python error.
3. Check whether Redis is available.
4. Verify the environment variables.
5. Install missing dependencies.
6. Restart FastAPI.
7. Open `/health`.
8. Test `/optimize-placement`.

---

### 15.3 Gemini recovery

If Gemini fails:

1. Check the FastAPI logs.
2. Verify that the API key is loaded.
3. Check the model name.
4. Check quota and permission.
5. Check internet connectivity.
6. Confirm that fallback explanation works.
7. Restart FastAPI after correcting the configuration.

The main optimization service should continue operating even when Gemini is unavailable.

---

## 16. Maintenance Incident Record

Use the following template:

```text
Maintenance ID:
Date:
Start time:
End time:
Maintenance performed by:
Services affected:
Reason for maintenance:
Actions performed:
Errors observed:
Corrective action:
Verification completed:
Final service status:
Additional recommendations:
```

Maintenance records provide evidence of operational activities and help identify repeated problems.

---

## 17. Final Maintenance Checklist

Before completing maintenance:

- [ ] Redis is running.
- [ ] Redis returns `PONG`.
- [ ] FastAPI starts successfully.
- [ ] `/health` shows a healthy status.
- [ ] `/optimize-placement` returns `200`.
- [ ] Redis caching works.
- [ ] Gemini works or fallback is available.
- [ ] No important errors appear in logs.
- [ ] Response time is acceptable.
- [ ] `.env` remains protected.
- [ ] Documentation is updated.
- [ ] Changes are committed to GitHub.
- [ ] No credentials are included in the commit.

---

## 18. Conclusion

The maintenance procedures described in this guide help keep the AdStream Revenue Optimization Platform reliable, secure, and efficient.

Daily maintenance verifies service availability and basic API functionality. Weekly maintenance focuses on Redis memory, logs, security, and fallback behaviour. Monthly maintenance evaluates dependencies, system performance, security, recovery, and documentation.

Regular load testing helps determine whether the system continues to support expected traffic. Redis caching improves response time, while the Gemini fallback mechanism ensures that the main optimization service remains available during an external LLM failure.

Following this guide reduces downtime, improves operational readiness, protects sensitive information, and supports the long-term scalability of the AdStream platform.