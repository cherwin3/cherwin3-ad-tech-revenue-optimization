from locust import HttpUser, task, between


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
            "user_id": "load_test_user",
            "page_id": "article_101",
            "scroll_depth": 65,
            "time_on_page": 45,
            "device_type": "desktop",
            "page_type": "news"
        }

        self.client.post(
            "/optimize-placement",
            json=payload,
            name="POST /optimize-placement"
        )