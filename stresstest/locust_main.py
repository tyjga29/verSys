from locust import HttpUser, task, between
import json

class MyUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 3)

    @task
    def search_and_verify(self):
        with self.client.get("/search_whole/", catch_response=True) as response:  # sending GET request to the specified endpoint
            try:
                data = response.json()
                if "result" in data and isinstance(data["result"], list) and len(data["result"]) == 1:
                    result = data["result"][0]
                    if "_id" in result and "sensorid" in result and "timestamp" in result and "unit" in result and "value" in result:
                        response.success()
                    else:
                        response.failure("Wrong Format of JSON")
                else:
                    response.failure("Wrong Format of JSON")
            except json.JSONDecodeError:
                response.failure("Failed to parse JSON")

