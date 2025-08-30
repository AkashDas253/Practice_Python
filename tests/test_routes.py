import unittest
from app.routes import home, about, contact, form, submit

class TestRoutes(unittest.TestCase):
    def test_home(self):
        self.assertIn(b"Hello, World!", home())
    def test_about(self):
        self.assertIn(b"About Page", about())
    def test_contact(self):
        self.assertIn(b"contact@example.com", contact())
    def test_form(self):
        self.assertIn(b"<form", form())
    def test_submit(self):
        post_data = "username=TestUser"
        response = submit(post_data)
        self.assertIn(b"Hello, TestUser!", response)

if __name__ == "__main__":
    unittest.main()
