import unittest
import os
import json
from contact_manager import ContactManager, Contact

class TestContactManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_contacts.json"
        self.manager = ContactManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_contact(self):
        self.manager.add_contact("John Doe", "1234567890", "john@example.com", "123 Main St")
        self.assertEqual(len(self.manager.contacts), 1)
        self.assertEqual(self.manager.contacts[0].name, "John Doe")
        self.assertEqual(self.manager.contacts[0].phone, "1234567890")

    def test_search_contact(self):
        self.manager.add_contact("Alice Smith", "9876543210", "alice@example.com", "456 Elm St")
        self.manager.add_contact("Bob Jones", "5555555555", "bob@example.com", "789 Oak St")
        
        # Test search by name
        results_name = [c for c in self.manager.contacts if "alice" in c.name.lower()]
        self.assertEqual(len(results_name), 1)
        self.assertEqual(results_name[0].name, "Alice Smith")

        # Test search by phone
        results_phone = [c for c in self.manager.contacts if "5555" in c.phone]
        self.assertEqual(len(results_phone), 1)
        self.assertEqual(results_phone[0].name, "Bob Jones")

    def test_delete_contact(self):
        self.manager.add_contact("Charlie Brown", "1111111111", "charlie@example.com", "321 Pine St")
        self.manager.delete_contact("Charlie Brown")
        self.assertEqual(len(self.manager.contacts), 0)

    def test_persistence(self):
        self.manager.add_contact("Dave Wilson", "2222222222", "dave@example.com", "654 Cedar St")
        # Create a new manager instance to simulate restarting the app
        new_manager = ContactManager(self.test_file)
        self.assertEqual(len(new_manager.contacts), 1)
        self.assertEqual(new_manager.contacts[0].name, "Dave Wilson")

if __name__ == '__main__':
    unittest.main()
