import unittest
from unittest.mock import patch, MagicMock

from eldom.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://myeldom.com"
        self.client = Client(base_url=self.base_url)
        self.email = "user@yahoo.com"
        self.password = "pass"
        self.device_id = "EDAB63C696969"
        self.state = 0

    @patch('client.requests.Session.post')
    def test_login(self, mock_post):
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        # Call the login method
        self.client.login(self.email, self.password)

        # Assert the post request was called with the correct parameters
        mock_post.assert_called_once_with(
            f"{self.base_url}/Account/Login",
            data={'Email': self.email, 'Password': self.password}
        )

    @patch('client.requests.Session.get')
    def test_get_devices(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"devices": []}
        mock_get.return_value = mock_response

        # Call the get_devices method
        response = self.client.get_devices()

        # Assert the get request was called with the correct parameters
        mock_get.assert_called_once_with(
            f"{self.base_url}/api/device/getmy",
            timeout=self.client.timeout
        )
        self.assertEqual(response, {"devices": []})

    @patch('client.requests.Session.post')
    def test_get_device(self, mock_post):
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"device": {}}
        mock_post.return_value = mock_response

        # Call the get_device method
        response = self.client.get_device(self.device_id)

        # Assert the post request was called with the correct parameters
        mock_post.assert_called_once_with(
            f"{self.base_url}/api/device/getmydevice",
            json={'deviceId': self.device_id}
        )
        self.assertEqual(response, {"device": {}})

    @patch('client.requests.Session.post')
    def test_set_device_state(self, mock_post):
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        # Call the set_device_state method
        response = self.client.set_flat_boiler_state(self.device_id, self.state)

        # Assert the post request was called with the correct parameters
        mock_post.assert_called_once_with(
            f"{self.base_url}/api/flatboiler/setState",
            json={'deviceId': self.device_id, 'state': self.state}
        )
        self.assertEqual(response, {"status": "success"})

if __name__ == '__main__':
    unittest.main()
