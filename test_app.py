from unittest import TestCase
from flask import session

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session["high_score"] = 500

            # test that you're getting a template
            response = client.get('/')

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<!-- HOMEPAGE Template for testing -->", html)
            self.assertIn("<table", html)
            self.assertIn("<title>Boggle</title>", html)
            self.assertEqual(session["high_score"], 500)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.post('/api/new-game')
            game_data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertIn("gameId", game_data)
            self.assertIsNotNone(game_data["board"])
            self.assertIsNotNone(game_data["gameId"])


