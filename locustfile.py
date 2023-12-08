from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/index.php?action=form1")
        self.client.get("/index.php?action=form2")
