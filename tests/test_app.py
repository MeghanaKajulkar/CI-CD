import unittest
from app import app

class TestFeedbackApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_feedback(self):
        response = self.app.post('/add_feedback', data=dict(name="Test User", message="Test Message"))
        self.assertEqual(response.status_code, 302)  # Redirect to home

if __name__ == '__main__':
    unittest.main()
