import unittest
import requests
from concurrent.futures import ThreadPoolExecutor

class Ratelimit(unittest.TestCase):
    def test_ratelimit(self):
        url = "http://localhost:8000/pokemon/Bulbasaur"

        def make_request():
            return requests.get(url)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in futures]

        statuses = []

        for response in responses:
            statuses.append(response.status_code)

        self.assertIn(429, statuses)


if __name__ == '__main__':
    unittest.main()
