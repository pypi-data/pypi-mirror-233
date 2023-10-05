import json, os, requests
from urllib.parse import quote

class FactCheck:
    def __init__(self, environment="prod"):
        if environment == "prod":
            self.base_url = "https://brainchain--fact-check.modal.run/fact-check"
        else:  # Assuming any other value refers to a dev environment
            self.base_url = "http://localhost:8000"

    def fact_check(self, statement):
        url = f"{self.base_url}"
        response = requests.post(url, headers={"Accept": "application/json"}, json={"statement": statement})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()