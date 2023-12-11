from locust import HttpUser, task
from termcolor import colored


class HelloWorldUser(HttpUser):
    @task
    def form_1_information_about_yourself_page(self):
        self.client.get("/index.php?action=form1")

    @task
    def form_2_accommodation_booking_form_page(self):
        self.client.get("/index.php?action=form2")

    @task
    def form_3_credit_card_page(self):
        self.client.get("/index.php?action=form3")

    @task
    def form_4_login_page(self):
        self.client.get("/index.php?action=form4")

        post_data = {'user': "admin", 'pw': 'pw1234'}
        with self.client.post('/en/login', post_data, catch_response=True) as response:
            if response.status_code != 200: print(
                colored("Expected 200 but got {}".format(response.status_code), 'red'))
