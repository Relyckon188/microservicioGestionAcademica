from locust import HttpUser, task, between
from locust.runners import STATE_STOPPED
import time

class SpikeUser(HttpUser):
    wait_time = between(1, 1)  # espera mínima entre tareas

    @task
    def post_request(self):
        BASE_URL = "https://ecommerce.universidad.localhost"  # cambiar URL

        payload = {"producto": 1, "cantidad": 1, "entrada_salida": 1}
        headers = {"Content-Type": "application/json"}

        with self.client.post("/", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Error: status={response.status_code}, payload={payload}")

# locust -f locust_tests/locustfile.py --host=https://ecommerce.universidad.localhost --users 100 --spawn-rate 10 --run-time 40s --headless
# locust -f locust_tests/locustfile.py --users 100 --spawn-rate 10 --run-time 40s --headless --html reporte.html
