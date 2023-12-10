# locust-python-example
Sample implementation of Python Locust performance testing.

## Application under test
The tests were written for https://github.com/andreasneuber/automatic-test-sample-site.
Readme in that repo has further details how to set it up.

## Setup
```
pip install locust

locust -V
```

## Run tests via WebUI
Tests are located in locustfile.py

Make sure you are in root folder of project, execute in terminal: `locust` then open http://localhost:8089/ in browser, 
add http://localhost:8000 as host url.

## Run tests in terminal
`locust -f locustfile.py --headless --host http://localhost:8000 --users 100 --spawn-rate 5`

## CI
As a matter of principle - whatever can be run in terminal can be run in a pipeline ;-)

## Docu
[https://docs.locust.io/en/stable/quickstart.html](https://docs.locust.io/en/stable/quickstart.html)
