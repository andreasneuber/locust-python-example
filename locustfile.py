from locust import HttpUser, task
from termcolor import colored
from faker import Faker
import time
import random
import re

# Initialize Faker for generating test data
fake = Faker()


class HelloWorldUser(HttpUser):
    host = "http://localhost:5000"

    @task
    def form_1_complete_user_journey(self):
        """Complete user journey: navigate to form1, fill data, submit, validate success"""
        # Step 1: Navigate to form1 page
        with self.client.get("/form1", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(colored(f"Failed to load form1 page. Expected 200 but got {response.status_code}", 'red'))
                return
            else:
                csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
                csrf_token = csrf_token.group(1) if csrf_token else ''
                response.success()
        
        # Step 2: Simulate user reading and thinking about the form (1-3 seconds)
        time.sleep(random.uniform(1, 3))
        
        # Step 3: Generate randomized test data
        form_data = {
            'csrf_token': csrf_token,
            'fname': fake.first_name(),
            'lname': fake.last_name(),
            'street': fake.street_address(),
            'city': fake.city(),
            'zip': fake.zipcode(),
            'state': fake.state(),
            'country': fake.country(),
            'mobile': fake.phone_number(),
            'home': fake.phone_number(),
            'email': fake.email()
        }
        
        # Step 4: Submit the form
        with self.client.post('/thankYou', form_data, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(colored(f"Form submission failed. Expected 200 but got {response.status_code}", 'red'))
                print(colored(f"Failed submission with data: {form_data}", 'red'))
            elif 'thank' not in response.text.lower():
                response.failure(colored("Thank you message not found in response", 'red'))
                print(colored(f"Response text: {response.text[:200]}", 'yellow'))
            else:
                response.success()
                print(colored(f"✓ Form submitted successfully for {form_data['fname']} {form_data['lname']}", 'green'))
    
    @task
    def form_1_information_about_yourself_page(self):
        self.client.get("/form1")

    @task
    def form_2_accommodation_booking_form_page(self):
        self.client.get("/form2")

    @task
    def form_3_credit_card_page(self):
        self.client.get("/form3")

    @task
    def form_4_login_page(self):
        with self.client.get("/form4", catch_response=True) as response:
            csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
            csrf_token = csrf_token.group(1) if csrf_token else ''
            response.success()

        post_data = {'csrf_token': csrf_token, 'user': "admin", 'pw': 'pw1234'}
        with self.client.post('/useraccount', post_data, catch_response=True) as response:
            if response.status_code != 200: print(
                colored("Expected 200 but got {}".format(response.status_code), 'red'))
