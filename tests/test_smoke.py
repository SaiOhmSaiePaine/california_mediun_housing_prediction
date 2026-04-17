import unittest

from app import app


class SmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page_loads(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('California House Price Prediction', response.get_data(as_text=True))

    def test_predict_api_returns_json_number(self):
        payload = {
            'data': {
                'MedInc': 8.3252,
                'HouseAge': 41.0,
                'AveRooms': 6.984,
                'AveBedrms': 1.024,
                'Population': 322.0,
                'AveOccup': 2.555,
                'Latitude': 37.88,
                'Longitude': -122.23,
            }
        }

        response = self.client.post('/predict_api', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertIsInstance(response.get_json(), float)

    def test_predict_form_renders_prediction(self):
        form_data = {
            'MedInc': '8.3252',
            'HouseAge': '41.0',
            'AveRooms': '6.984',
            'AveBedrms': '1.024',
            'Population': '322.0',
            'AveOccup': '2.555',
            'Latitude': '37.88',
            'Longitude': '-122.23',
        }

        response = self.client.post('/predict', data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('The predicted price of the house is', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
