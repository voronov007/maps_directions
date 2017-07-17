import unittest
import json

from app import app


class TestDirections(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_request(self):
        # origin - Kyiv
        # destination - Brussels
        data = {
            'origin': [50.455208, 30.355092],
            'destination': [50.850329, 4.351687]
        }
        data_json = json.dumps(data)
        directions = self.app.post('/directions', data=data_json,
                                   headers={"Content-Type": "application/json"})
        result = json.loads(directions.data)
        print(result)
        if result.get('message'):
            self.fail('Error during request to the Google Maps')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
