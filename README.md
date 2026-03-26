# Locust Python Example
A sample implementation of Locust performance testing in Python.

## Application under test
The tests were written for https://github.com/andreasneuber/automatic-test-sample-site
The README in that repo has further details on how to set it up.


## Setup
Clone the repo and set up the virtual environment and dependencies as follows:

```powershell
# Clone the repository
git clone <repo-url>
cd locust-python-example

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify Locust installation
locust -V
```

After activation, you should see a `(.venv)` prefix in your terminal prompt.

## Run tests via WebUI
Tests are located in `locustfile.py`

Make sure you are in the root folder of the project, execute in terminal: `locust` then open http://localhost:8089/ in a browser, 
and add http://localhost:8000 as the host URL.

## Run tests in terminal
`locust -f locustfile.py --headless --host http://localhost:8000 --users 100 --spawn-rate 5`

## CI
As a matter of principle - whatever can be run in a terminal can be run in a pipeline ;-)

## Documentation
[https://docs.locust.io/en/stable/quickstart.html](https://docs.locust.io/en/stable/quickstart.html)
