    python -m venv venv

    pip install -r requirements.txt

    pytest ./src/API_unit_test.py

    locust -f .src/testing/perfomence_test.py

    go to http://0.0.0.0:8089/
