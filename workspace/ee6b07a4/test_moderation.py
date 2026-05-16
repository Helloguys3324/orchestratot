import unittest
import os
from moderation_service import ModerationService

class TestModerationService(unittest.TestCase):
    def setUp(self):
        self.log_file = "test_moderation.log"
        self.service = ModerationService(self.log_file)

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_log_creation(self):
        self.service.log_deletion("123", "user1", "hello")
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            content = f.read()
            self.assertIn("123", content)
            self.assertIn("user1", content)
            self.assertIn("hello", content)

    def test_file_permissions(self):
        # Check if file is restricted (octal 600)
        mode = os.stat(self.log_file).st_mode & 0o777
        self.assertEqual(mode, 0o600)

if __name__ == '__main__':
    unittest.main()