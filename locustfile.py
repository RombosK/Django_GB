from locust import HttpUser, task

SERVER_IP_ADDR = '134.0.113.9'


class LoadTestingBraniacLMS(HttpUser):
    @task
    def some_pages_open(self):
        self.client.get(f"http://{SERVER_IP_ADDR}/home/")
        self.client.get(f"http://{SERVER_IP_ADDR}/home/courses")
        self.client.get(f"http://{SERVER_IP_ADDR}/home/news/")
        self.client.get(f"http://{SERVER_IP_ADDR}/home/courses/3/detail")

        self.client.get(f"http://{SERVER_IP_ADDR}/authapp/register")
        self.client.get(f"http://{SERVER_IP_ADDR}/authapp/login/")

