import unittest
from flask import Flask, jsonify
from flask_testing import TestCase
from RestApi import app, mongo  # Replace 'your_app_file' with the actual filename of your Flask app

class TestAPI(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["MONGO_URI"] = "mongodb://localhost:27017/gradebook_test"  # Use a test database
        return app

    def setUp(self):
        mongo.db.gradebook.drop()  # Clear the test database before each test

    def tearDown(self):
        mongo.db.gradebook.drop()  # Clear the test database after each test

    def test_add_result(self):
        # Test adding a result via POST request
        data = {"roll_no": "123", "name": "John Doe", "score": 95}
        response = self.client.post("/results", json=data)
        self.assert200(response)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Result added successfully")

    def test_get_results(self):
        # Test retrieving results via GET request
        data = {"roll_no": "123", "name": "John Doe", "score": 95}
        self.client.post("/results", json=data)  # Add a result for testing
        response = self.client.get("/results")
        self.assert200(response)
        self.assertIn("results", response.json)
        results = response.json["results"]
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertDictEqual(results[0], data)

    def test_update_result(self):
        # Test updating a result via PUT request
        initial_data = {"roll_no": "123", "name": "John Doe", "score": 95}
        updated_data = {"roll_no": "123", "name": "John Updated", "score": 98}
        self.client.post("/results", json=initial_data)  # Add a result for testing
        response = self.client.put("/results/123", json=updated_data)
        self.assert200(response)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Result updated successfully")

        # Verify that the result has been updated
        updated_response = self.client.get("/results")
        updated_results = updated_response.json["results"]
        self.assertEqual(len(updated_results), 1)
        self.assertDictEqual(updated_results[0], updated_data)

    def test_delete_result(self):
        # Test deleting a result via DELETE request
        data = {"roll_no": "123", "name": "John Doe", "score": 95}
        self.client.post("/results", json=data)  # Add a result for testing
        response = self.client.delete("/results/123")
        self.assert200(response)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Result deleted successfully")

        # Verify that the result has been deleted
        deleted_response = self.client.get("/results")
        deleted_results = deleted_response.json["results"]
        self.assertEqual(len(deleted_results), 0)

if __name__ == "__main__":
    unittest.main()
